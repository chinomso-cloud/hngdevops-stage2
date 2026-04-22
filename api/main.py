from fastapi import FastAPI
import redis
import uuid
import os

app = FastAPI()


r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379))
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/jobs")
def create_job():
    job_id = str(uuid.uuid4())
    r.lpush("jobs_queue", job_id)
    r.hset(f"job:{job_id}", "status", "queued")
    return {"job_id": job_id}


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    status = r.hget(f"job:{job_id}", "status")
    if not status:
        return {"error": "not found"}
    return {"job_id": job_id, "status": status.decode()}




same thing with your worker as well and replace with this 


import redis
import time
import os
import signal
import sys


r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379))
)


def process_job(job_id):
    try:
        print(f"Processing job {job_id}")
        time.sleep(2)
        r.hset(f"job:{job_id}", "status", "completed")
        print(f"Done: {job_id}")
    except Exception as e:
        r.hset(f"job:{job_id}", "status", "failed")
        print(f"Failed job {job_id}: {e}")


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
