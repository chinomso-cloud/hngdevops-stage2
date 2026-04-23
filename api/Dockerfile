# -------- BUILD STAGE --------
FROM python:3.11-slim AS builder

WORKDIR /app

# DL3042: Fixed with --no-cache-dir
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


# -------- RUNTIME STAGE --------
FROM python:3.11-slim

WORKDIR /app

# DL3008: Pinned to Candidate 8.14.1-2+deb13u2
# DL3015: Added --no-install-recommends
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl=8.14.1-2+deb13u2 && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m appuser
USER appuser

# Copy installed packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy app source code
COPY . .

# PATH fix
ENV PATH=/home/appuser/.local/bin:$PATH

# ENV vars
ENV REDIS_HOST=localhost
ENV REDIS_PORT=6379

EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
  CMD curl --fail http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"