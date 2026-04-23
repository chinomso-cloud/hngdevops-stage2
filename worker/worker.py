import redis
import time
import os
import signal
import sys

# -------------------------
# REDIS CONNECTION
# -------------------------
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

running = True


# -------------------------
# GRACEFUL SHUTDOWN
# -------------------------
def shutdown(signum, frame):
    global running
    print("Shutting down worker...")
    running = False


signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)


# -------------------------
# PROCESS JOB
# -------------------------
def process_job(job_id):
    try:
        print(f"Processing job {job_id}")

        # mark processing
        r.hset(f"job:{job_id}", "status", "processing")

        time.sleep(2)  # simulate work

        # ? FIX: must match integration test expectation
        r.hset(f"job:{job_id}", "status", "done")

        print(f"Completed job {job_id}")

    except Exception as e:
        print(f"Error processing job {job_id}: {e}")
        r.hset(f"job:{job_id}", "status", "failed")


# -------------------------
# WORKER LOOP
# -------------------------
print("Worker started...")

while running:
    try:
        job = r.brpop("jobs", timeout=5)

        if job:
            _, job_id = job
            process_job(job_id)

    except redis.exceptions.ConnectionError:
        print("Redis connection error. Retrying...")
        time.sleep(2)

    except Exception as e:
        print(f"Unexpected error: {e}")
        time.sleep(2)

print("Worker stopped cleanly.")
sys.exit(0)
