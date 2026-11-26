FROM python:3.12-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1 HF_HOME=/opt/hf

# CPU-only PyTorch first, so sentence-transformers does not pull the much larger GPU build.
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download the embedding model at build time (keep in step with ragdemo.index.DEFAULT_MODEL).
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-small-en-v1.5')"

COPY pyproject.toml .
COPY src ./src
RUN pip install --no-cache-dir --no-deps .

RUN useradd --create-home appuser && chown -R appuser /opt/hf
USER appuser

# data/ (chunks.jsonl and index.faiss) is not in the image: mount it at /app/data.
EXPOSE 8000
CMD ["uvicorn", "ragdemo.api:app", "--host", "0.0.0.0", "--port", "8000"]
