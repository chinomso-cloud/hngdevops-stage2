from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)


@patch("main.r")
def test_create_job(mock_redis):
    mock_redis.lpush = MagicMock(return_value=1)
    mock_redis.hset = MagicMock(return_value=1)

    response = client.post("/jobs")

    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert isinstance(data["job_id"], str)


@patch("main.r")
def test_health(mock_redis):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("main.r")
def test_get_job_invalid(mock_redis):
    mock_redis.hget = MagicMock(return_value=None)

    response = client.get("/jobs/invalid-id")

    assert response.status_code == 200
    assert response.json() == {"error": "not found"}
