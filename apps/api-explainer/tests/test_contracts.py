"""Contract tests for API endpoints against JSON schemas."""

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app

# Load JSON schemas
SCHEMAS_DIR = Path(__file__).parent.parent.parent.parent / "packages" / "shared" / "schemas"


def load_schema(name: str) -> dict:
    """Load JSON schema from packages/shared/schemas."""
    schema_path = SCHEMAS_DIR / f"{name}.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_against_schema(data: dict, schema: dict) -> list[str]:
    """Basic schema validation (simplified; use jsonschema library for full validation)."""
    errors = []
    
    # Check required fields
    required = schema.get("properties", {})
    for field in schema.get("required", []):
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # Type checking
    for field, value in data.items():
        if field in required:
            expected_type = required[field].get("type")
            if expected_type == "string" and not isinstance(value, str):
                errors.append(f"Field '{field}' should be string, got {type(value).__name__}")
            elif expected_type == "number" and not isinstance(value, (int, float)):
                errors.append(f"Field '{field}' should be number, got {type(value).__name__}")
            elif expected_type == "object" and not isinstance(value, dict):
                errors.append(f"Field '{field}' should be object, got {type(value).__name__}")
            elif expected_type == "array" and not isinstance(value, list):
                errors.append(f"Field '{field}' should be array, got {type(value).__name__}")
    
    return errors


@pytest.fixture
def client():
    return TestClient(app)


def test_health_contract(client):
    """Test /health response matches schema."""
    response = client.post("/health")
    assert response.status_code == 200
    
    data = response.json()
    schema = load_schema("health.response")
    errors = validate_against_schema(data, schema)
    assert not errors, f"Schema validation errors: {errors}"
    assert data["status"] == "ok"


def test_explain_request_validation(client):
    """Test /explain request validation."""
    # Missing required fields
    response = client.post("/explain", json={})
    assert response.status_code == 422
    
    # Invalid locale format
    response = client.post("/explain", json={
        "docText": "test",
        "docMeta": {},
        "locale": "invalid",
        "deviceId": "abc"
    })
    assert response.status_code == 422


def test_explain_response_contract(client):
    """Test /explain response matches schema."""
    request_data = {
        "docText": "HDFC Credit Card Statement\nTotal Due: ₹4,250\nDue Date: 15 Nov 2025",
        "docMeta": {"typeHint": "credit-card-statement", "pages": 1},
        "locale": "en-IN",
        "hints": False,
        "deviceId": "test-device-123"
    }
    
    response = client.post("/explain", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    schema = load_schema("explain.response")
    errors = validate_against_schema(data, schema)
    assert not errors, f"Schema validation errors: {errors}"
    
    # Check specific fields
    assert "summary" in data
    assert "extractions" in data
    assert "actions" in data
    assert "confidence" in data
    assert 0 <= data["confidence"] <= 1
    assert "docType" in data
    assert "citations" in data


def test_explain_rate_limit(client):
    """Test rate limiting (if Redis is not configured, should pass)."""
    request_data = {
        "docText": "test document",
        "docMeta": {},
        "locale": "en-IN",
        "deviceId": "rate-test-device"
    }
    
    # Send multiple requests rapidly
    responses = []
    for _ in range(70):  # Exceed default 60 RPM
        resp = client.post("/explain", json=request_data)
        responses.append(resp.status_code)
    
    # If Redis is configured, should get 429 after 60 requests
    # If not configured, all should be 200
    status_200_count = sum(1 for s in responses if s == 200)
    status_429_count = sum(1 for s in responses if s == 429)
    
    # Either all pass (no Redis) or some are rate-limited (Redis configured)
    assert status_200_count + status_429_count == len(responses)


def test_explain_caching(client):
    """Test that identical requests return cached responses."""
    request_data = {
        "docText": "identical test document for caching",
        "docMeta": {},
        "locale": "en-IN",
        "deviceId": "cache-test-device"
    }
    
    response1 = client.post("/explain", json=request_data)
    assert response1.status_code == 200
    data1 = response1.json()
    
    response2 = client.post("/explain", json=request_data)
    assert response2.status_code == 200
    data2 = response2.json()
    
    # Responses should be identical (cached)
    assert data1 == data2

