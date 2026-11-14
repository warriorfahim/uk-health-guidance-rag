"""Hugging Face hosted LLM (Inference Providers) as a `generate(prompt) -> str` callable."""
import os

DEFAULT_MODEL = "meta-llama/Llama-3.1-8B-Instruct"


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
