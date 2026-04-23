from fastapi import FastAPI
import redis
import uuid
import os

app = FastAPI()

# -------------------------
# FIX: correct docker redis host
# -------------------------
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)


# -------------------------
# HEALTH CHECK
# -------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# -------------------------
# CREATE JOB
# -------------------------
@app.post("/jobs")
def create_job():
    job_id = str(uuid.uuid4())

    # queue job first
    r.lpush("jobs", job_id)

    # store metadata
    r.hset(f"job:{job_id}", mapping={"status": "queued"})

    return {"job_id": job_id}


# -------------------------
# GET JOB STATUS
# -------------------------
@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    status = r.hget(f"job:{job_id}", "status")

    if not status:
        return {"error": "not found"}

    return {
        "job_id": job_id,
        "status": status
    }
