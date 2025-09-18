from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_student():
    response = client.post(
        "/students/",
        json={
            "name": "Test Student",
            "dob": "2012-01-01",
            "disabilities": [],
            "baseline_skills": {"math": "basic"}
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Student"
    assert "id" in data


def test_list_students():
    response = client.get("/students/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
