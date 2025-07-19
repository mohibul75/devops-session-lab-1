from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/v1/api")
    assert response.status_code == 200
    assert response.json() == {"message": "hello form hands on session lab 1"}