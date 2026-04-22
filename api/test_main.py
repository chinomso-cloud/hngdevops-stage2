from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# 1. Test job creation
def test_create_job():
    response = client.post("/jobs")
    assert response.status_code == 200
    assert "job_id" in response.json()


# 2. Test health endpoint
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# 3. Test get job (invalid id)
def test_get_job_invalid():
    response = client.get("/jobs/invalid-id")
    assert response.status_code == 200
    assert "error" in response.json()