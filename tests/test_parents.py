from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_parent():
    response = client.post(
        "/parents/",
        json={
            "name": "Parent One",
            "email": "parent1@example.com",
            "phone": "555-1234"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Parent One"
    assert data["email"] == "parent1@example.com"
    assert "id" in data


def test_list_parents():
    response = client.get("/parents/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_parent():
    create_resp = client.post(
        "/parents/",
        json={
            "name": "Parent Two",
            "email": "parent2@example.com",
            "phone": "555-5678"
        }
    )
    parent_id = create_resp.json()["id"]
    response = client.get(f"/parents/{parent_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Parent Two"


def test_update_parent():
    create_resp = client.post(
        "/parents/",
        json={
            "name": "Parent Three",
            "email": "parent3@example.com",
            "phone": "555-9999"
        }
    )
    parent_id = create_resp.json()["id"]
    response = client.put(
        f"/parents/{parent_id}",
        json={
            "name": "Parent Three Updated",
            "email": "parent3@example.com",
            "phone": "555-0000"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Parent Three Updated"
    assert data["phone"] == "555-0000"


def test_delete_parent():
    create_resp = client.post(
        "/parents/",
        json={
            "name": "Parent Four",
            "email": "parent4@example.com",
            "phone": "555-1111"
        }
    )
    parent_id = create_resp.json()["id"]
    response = client.delete(f"/parents/{parent_id}")
    assert response.status_code == 200
    # Should not find after delete
    get_resp = client.get(f"/parents/{parent_id}")
    assert get_resp.status_code == 404


def test_parent_student_relationship():
    # Create parent
    parent_resp = client.post(
        "/parents/",
        json={
            "name": "Parent Five",
            "email": "parent5@example.com",
            "phone": "555-2222"
        }
    )
    parent_id = parent_resp.json()["id"]
    # Create student and assign parent
    student_resp = client.post(
        "/students/",
        json={
            "name": "Child One",
            "dob": "2013-05-01",
            "disabilities": [],
            "baseline_skills": {},
            "parents": [parent_id]
        }
    )
    student_id = student_resp.json()["id"]
    # Check parent->students endpoint
    resp = client.get(f"/parents/{parent_id}/students")
    assert resp.status_code == 200
    students = resp.json()
    assert any(s["id"] == student_id for s in students)
    # Update student parents
    resp2 = client.put(f"/students/{student_id}/parents", json=[parent_id])
    assert resp2.status_code == 200
    # Remove parent
    resp3 = client.put(f"/students/{student_id}/parents", json=[])
    assert resp3.status_code == 200
    # Now parent->students should be empty
    resp4 = client.get(f"/parents/{parent_id}/students")
    assert resp4.status_code == 200
    assert resp4.json() == []
