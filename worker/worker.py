import redis
import time
import os
import signal
import sys

# Safe Redis connection (ENV-based)
r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379))
)

def process_job(job_id):
    try:
        print(f"Processing job {job_id}")

        time.sleep(2)  # simulate work

        r.hset(f"job:{job_id}", "status", "completed")

        print(f"Done: {job_id}")

    except Exception as e:
        r.hset(f"job:{job_id}", "status", "failed")
        print(f"Failed job {job_id}: {e}")

# Graceful shutdown handling
def shutdown(sig, frame):
    print("Shutting down worker...")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

print("Worker started... waiting for jobs")

while True:
    try:
        job = r.brpop("jobs_queue", timeout=5)

        if job:
            _, job_id = job
            process_job(job_id.decode())

    except Exception as e:
        print(f"Worker error: {e}")
        time.sleep(2)