"""LLM backends as `generate(prompt) -> str` callables: local Ollama (default), OpenRouter or Hugging Face."""
import json
import os
import time
import urllib.error
import urllib.request

DEFAULT_MODEL = "meta-llama/Llama-3.1-8B-Instruct"  # Hugging Face
OLLAMA_MODEL = "qwen2.5:7b"
OLLAMA_URL = "http://localhost:11434"
OPENROUTER_DEFAULT_MODEL = "baidu/ernie-5.5-flash-preview:free"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
BACKENDS = ("ollama", "openrouter", "hf", "none")


def make_hf_generate(
    model: str | None = None,
    token: str | None = None,
    max_tokens: int = 400,
    temperature: float = 0.1,
):
    """Return a `generate` function for `ragdemo.answer.answer`.

    The token is read from the HF_TOKEN environment variable (a free Hugging Face access token
    with permission to call Inference Providers). The model comes from `model`, then the
    HF_MODEL environment variable, then DEFAULT_MODEL.
    """
    token = token or os.environ.get("HF_TOKEN")
    if not token:
        raise RuntimeError("HF_TOKEN is not set. Create a free token at huggingface.co/settings/tokens.")
    model = model or os.environ.get("HF_MODEL") or DEFAULT_MODEL

    from huggingface_hub import InferenceClient  # lazy: keep heavy imports out of module import

    client = InferenceClient(model=model, token=token)

    def generate(prompt: str) -> str:
        resp = client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return resp.choices[0].message.content.strip()

    return generate


def make_ollama_generate(
    model: str | None = None,
    base_url: str | None = None,
    max_tokens: int = 400,
    temperature: float = 0.1,
    timeout: float = 300.0,
):
    """Return a `generate` function that calls a local Ollama server (standard library only).

    Model comes from `model`, then OLLAMA_MODEL, then "qwen2.5:7b". Server URL comes from
    `base_url`, then OLLAMA_URL, then http://localhost:11434. Pull the model first with
    `ollama pull qwen2.5:7b`.
    """
    model = model or os.environ.get("OLLAMA_MODEL") or OLLAMA_MODEL
    url = (base_url or os.environ.get("OLLAMA_URL") or OLLAMA_URL).rstrip("/") + "/api/chat"

    def generate(prompt: str) -> str:
        body = json.dumps({
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"num_predict": max_tokens, "temperature": temperature, "num_ctx": 4096},
        }).encode("utf-8")
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.load(resp)["message"]["content"].strip()

    return generate


def _retry_delay(exc: urllib.error.HTTPError, retry_wait: float, attempt: int) -> float:
    """Seconds to wait before retrying a rate-limited call (at most 60)."""
    header = exc.headers.get("Retry-After") if exc.headers else None
    try:
        wait = float(header) if header else retry_wait * (attempt + 1)
    except ValueError:
        wait = retry_wait * (attempt + 1)
    return min(wait, 60.0)


def make_openrouter_generate(
    model: str | None = None,
    api_key: str | None = None,
    max_tokens: int = 400,
    temperature: float = 0.1,
    timeout: float = 120.0,
    retries: int = 4,
    retry_wait: float = 15.0,
):
    """Return a `generate` function that calls OpenRouter (standard library only).

    The key is read from `api_key`, then the OPENROUTER_API_KEY environment variable. Model comes
    from `model`, then OPENROUTER_MODEL, then OPENROUTER_DEFAULT_MODEL. Note that the question and
    retrieved passages are sent to a third party.

    A rate-limited call (HTTP 429) is retried up to `retries` times. Each wait is the server's
    Retry-After header if it sends one, otherwise `retry_wait` seconds times the attempt number,
    and never more than 60 seconds.

    After each call, `generate.last_info` holds the reply's `finish_reason` and token `usage` as
    OpenRouter reported them (empty if the request itself failed).
    """
    api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set. Create a key at openrouter.ai/keys.")
    model = model or os.environ.get("OPENROUTER_MODEL") or OPENROUTER_DEFAULT_MODEL

    def generate(prompt: str) -> str:
        generate.last_info = {}
        body = json.dumps({
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }).encode("utf-8")
        req = urllib.request.Request(
            OPENROUTER_URL,
            data=body,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        )
        for attempt in range(retries + 1):
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    data = json.load(resp)
                break
            except urllib.error.HTTPError as exc:
                if exc.code == 429 and attempt < retries:
                    time.sleep(_retry_delay(exc, retry_wait, attempt))
                    continue
                hint = " (rate limited; try again shortly)" if exc.code == 429 else ""
                raise RuntimeError(f"OpenRouter returned HTTP {exc.code}{hint}") from exc
        choice = (data.get("choices") or [{}])[0]
        generate.last_info = {"finish_reason": choice.get("finish_reason"), "usage": data.get("usage")}
        content = choice.get("message", {}).get("content")
        if not content:
            raise RuntimeError("OpenRouter returned an empty answer")
        return content.strip()

    generate.last_info = {}
    return generate


def make_echo_generate(reason: str):
    """Fallback `generate` that makes no LLM call and returns the grounded prompt instead."""

    def generate(prompt: str) -> str:
        return f"No LLM available ({reason}). Grounded prompt that would be sent:\n\n{prompt}"

    return generate


def ollama_available(base_url: str | None = None, timeout: float = 1.0) -> bool:
    """True if an Ollama server answers at the configured URL."""
    url = (base_url or os.environ.get("OLLAMA_URL") or OLLAMA_URL).rstrip("/") + "/api/tags"
    try:
        with urllib.request.urlopen(url, timeout=timeout):
            return True
    except OSError:
        return False


def make_generate(backend: str | None = None, max_tokens: int = 400):
    """Pick a backend: the argument, else LLM_BACKEND, else "ollama".

    Choices are "ollama", "openrouter", "hf" or "none". Falls back to `make_echo_generate` (shows
    the grounded prompt) when the chosen backend is not usable: Ollama is not running, or
    "openrouter"/"hf" is selected without its key. "none" forces the fallback.
    `max_tokens` caps the length of each reply.
    """
    backend = (backend or os.environ.get("LLM_BACKEND", "ollama")).lower()
    if backend == "none":
        return make_echo_generate("LLM_BACKEND=none")
    if backend == "openrouter":
        if not os.environ.get("OPENROUTER_API_KEY"):
            return make_echo_generate("OPENROUTER_API_KEY is not set")
        return make_openrouter_generate(max_tokens=max_tokens)
    if backend == "hf":
        if not os.environ.get("HF_TOKEN"):
            return make_echo_generate("HF_TOKEN is not set")
        return make_hf_generate(max_tokens=max_tokens)
    if backend == "ollama":
        if not ollama_available():
            return make_echo_generate("Ollama is not running")
        return make_ollama_generate(max_tokens=max_tokens)
    raise RuntimeError(f"Unknown LLM_BACKEND {backend!r}; use one of {', '.join(BACKENDS)}.")
