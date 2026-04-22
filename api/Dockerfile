# -------- BUILD STAGE --------
FROM python:3.11-slim AS builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --user -r requirements.txt


# -------- RUNTIME STAGE --------
FROM python:3.11-slim

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m appuser
USER appuser

# Copy installed packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy app source code
COPY . .

# PATH fix
ENV PATH=/home/appuser/.local/bin:$PATH

# ENV vars (Docker override will still apply)
ENV REDIS_HOST=localhost
ENV REDIS_PORT=6379

EXPOSE 8000

# Healthcheck (FIXED)
HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
  CMD curl --fail http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]