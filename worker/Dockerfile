# -------- BASE IMAGE --------
FROM python:3.11-slim

WORKDIR /app

# Install system tools for healthcheck
RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m workeruser
USER workeruser

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --user -r requirements.txt

# Copy app
COPY . .

# PATH fix
ENV PATH=/home/workeruser/.local/bin:$PATH

# ENV variables (IMPORTANT: matches docker-compose)
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379

# Healthcheck (FIXED)
HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
  CMD pgrep -f worker.py || exit 1

CMD ["python", "worker.py"]