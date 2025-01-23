from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
from app.utils import create_new_html
import pytest 


def test_root():
    response=client.get("/")
    assert response.status_code ==200
    assert response.json() == {"hello":"world"}

