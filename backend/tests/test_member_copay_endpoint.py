from fastapi.testclient import TestClient
import pytest
from main import app, token_listener

app.dependency_overrides[token_listener] = lambda: {}
client = TestClient(app)

def test_api_base_api():
    response = client.get("/membercopay/1")
    assert response.status_code == 200
