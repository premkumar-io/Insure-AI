import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "active"
    assert "version" in data

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["OK", "DEGRADED"]
    assert data["model_loaded"] is True
    assert data["version"] == "2.0.0"

def test_predict_success():
    payload = {
        "age": 30,
        "weight": 68.0,
        "height": 1.75,
        "income_lpa": 12.5,
        "smoker": False,
        "city": "Mumbai",
        "occupation": "private_job"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_category" in data
    assert data["predicted_category"] in ["Low", "Medium", "High"]
    assert 0.0 <= data["confidence"] <= 1.0
    assert "class_probabilities" in data
    assert "Low" in data["class_probabilities"]

def test_predict_validation_error():
    payload = {
        "age": -5,  # Invalid negative age
        "weight": 68.0,
        "height": 1.75,
        "income_lpa": 12.5,
        "smoker": False,
        "city": "Mumbai",
        "occupation": "private_job"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert "details" in data["error"]

def test_vercel_serverless_entrypoint():
    from api.index import app as vercel_app
    vercel_client = TestClient(vercel_app)
    res = vercel_client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "OK"

