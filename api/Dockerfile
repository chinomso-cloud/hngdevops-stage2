# -------- BUILD STAGE --------
FROM python:3.11-slim AS builder

WORKDIR /app

# DL3042: Avoid use of cache directory with pip. 
# Added --no-cache-dir
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


# -------- RUNTIME STAGE --------
FROM python:3.11-slim

WORKDIR /app

# DL3008: Pin versions in apt-get install.
# DL3015: Avoid additional packages by specifying --no-install-recommends
# Note: Version 7.88.1-10+deb12u8 is standard for Debian 12 (Bookworm)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl=7.88.1-10+deb12u8 && \
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

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]