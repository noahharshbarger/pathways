from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_teacher():
    resp = client.post(
        "/teachers/",
        json={
            "name": "Test Teacher",
            "email": "teacher@example.com",
            "password_hash": "secret"
        }
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Test Teacher"
    assert data["email"] == "teacher@example.com"
    assert "id" in data


def test_get_teacher():
    # Create teacher
    resp = client.post(
        "/teachers/",
        json={
            "name": "Teacher2",
            "email": "teacher2@example.com",
            "password_hash": "secret"
        }
    )
    teacher_id = resp.json()["id"]
    # Get teacher
    resp = client.get(f"/teachers/{teacher_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == teacher_id


def test_delete_teacher():
    resp = client.post(
        "/teachers/",
        json={
            "name": "Teacher3",
            "email": "teacher3@example.com",
            "password_hash": "secret"
        }
    )
    teacher_id = resp.json()["id"]
    resp = client.delete(f"/teachers/{teacher_id}")
    assert resp.status_code == 200
    # Should not find after delete
    resp = client.get(f"/teachers/{teacher_id}")
    assert resp.status_code == 200
    assert resp.json() is None


def test_create_goal():
    # Create student and teacher
    student = client.post(
        "/students/",
        json={
            "name": "Goal Student",
            "dob": "2012-01-01",
            "disabilities": [],
            "baseline_skills": {}
        }
    ).json()
    client.post(
        "/teachers/",
        json={
            "name": "Goal Teacher",
            "email": "goalteacher@example.com",
            "password_hash": "secret"
        }
    )
    goal = {
        "type": "academic",
        "description": "Improve math",
        "target_date": "2025-12-31",
        "progress": 0,
        "student_id": student["id"]
    }
    resp = client.post("/goals/", json=goal)
    assert resp.status_code == 200
    data = resp.json()
    assert data["description"] == "Improve math"
    assert data["student_id"] == student["id"]


def test_create_note():
    student = client.post(
        "/students/",
        json={
            "name": "Note Student",
            "dob": "2012-01-01",
            "disabilities": [],
            "baseline_skills": {}
        }
    ).json()
    note = {
        "author": "Teacher",
        "content": "Great job!",
        "student_id": student["id"]
    }
    resp = client.post("/notes/", json=note)
    assert resp.status_code == 200
    data = resp.json()
    assert data["author"] == "Teacher"
    assert data["student_id"] == student["id"]


def test_get_notes_by_student():
    student = client.post(
        "/students/",
        json={
            "name": "Note2 Student",
            "dob": "2012-01-01",
            "disabilities": [],
            "baseline_skills": {}
        }
    ).json()
    note = {
        "author": "Teacher",
        "content": "Keep it up!",
        "student_id": student["id"]
    }
    client.post("/notes/", json=note)
    resp = client.get(f"/notes/student/{student['id']}")
    assert resp.status_code == 200
    notes = resp.json()
    assert any(n["content"] == "Keep it up!" for n in notes)
