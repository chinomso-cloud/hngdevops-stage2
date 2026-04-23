# -------- BUILD STAGE --------
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# -------- RUNTIME STAGE --------
FROM python:3.11-slim
WORKDIR /app

# Fixed DL3008 (Pinned version) & DL3015 (No-recommends)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl=8.14.1-2+deb13u2 && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m appuser
USER appuser
COPY --from=builder /root/.local /home/appuser/.local
COPY . .
ENV PATH=/home/appuser/.local/bin:$PATH
EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
  CMD curl --fail http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]