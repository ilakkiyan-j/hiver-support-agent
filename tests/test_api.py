import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_api_health():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "version" in data

def test_api_brands():
    res = client.get("/api/v1/brands")
    assert res.status_code == 200
    data = res.json()
    assert data["count"] >= 1

def test_api_analyze_conversation():
    payload = {
        "brand_id": "AppleSupport",
        "customer_message": "My battery is dying fast after updating to iOS 11"
    }
    res = client.post("/api/v1/conversations/analyze", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "run_id" in data
    assert "intent" in data
    assert "decision" in data
    assert "evidence" in data

def test_api_experiments():
    exp_payload = {
        "name": "test_exp_01",
        "description": "Test experiment endpoint"
    }
    res = client.post("/api/v1/experiments", json=exp_payload)
    assert res.status_code == 200
    exp_data = res.json()
    assert "experiment_id" in exp_data

    res_list = client.get("/api/v1/experiments")
    assert res_list.status_code == 200
    assert res_list.json()["count"] >= 1
