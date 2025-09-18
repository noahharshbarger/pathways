from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_iep():
    # Create a student first (required foreign key)
    student_resp = client.post(
        "/students/",
        json={
            "name": "IEP Student",
            "dob": "2012-01-01",
            "disabilities": [],
            "baseline_skills": {"math": "basic"}
        }
    )
    assert student_resp.status_code == 200
    student_id = student_resp.json()["id"]

    # Create IEP
    iep_data = {
        "student_id": student_id,
        "data": {"goals": ["Goal 1"], "services": ["Speech"]},
        "created_by": "test_teacher"
    }
    resp = client.post("/ieps/", json=iep_data)
    assert resp.status_code == 200
    data = resp.json()
    assert data["student_id"] == student_id
    assert data["created_by"] == "test_teacher"
    assert "id" in data


def test_create_progress_log():
    # Create a student and IEP first
    student_resp = client.post(
        "/students/",
        json={
            "name": "Progress Student",
            "dob": "2012-01-01",
            "disabilities": [],
            "baseline_skills": {"math": "basic"}
        }
    )
    assert student_resp.status_code == 200
    student_id = student_resp.json()["id"]

    iep_resp = client.post(
        "/ieps/",
        json={
            "student_id": student_id,
            "data": {"goals": ["Goal 1"]},
            "created_by": "test_teacher"
        }
    )
    assert iep_resp.status_code == 200
    iep_id = iep_resp.json()["id"]

    # Create Progress Log
    log_data = {
        "iep_id": iep_id,
        "data": {"log": "Student made progress."},
        "created_by": "test_teacher"
    }
    resp = client.post("/progress/", json=log_data)
    assert resp.status_code == 200
    data = resp.json()
    assert data["iep_id"] == iep_id
    assert data["created_by"] == "test_teacher"
    assert "id" in data
