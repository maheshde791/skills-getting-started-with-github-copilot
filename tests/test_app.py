from fastapi.testclient import TestClient
import pytest

from src.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # each activity should have participants key
    for v in data.values():
        assert "participants" in v


def test_signup_and_unregister_flow(client):
    activity = "Chess Club"
    email = "test_student@example.com"

    # ensure not present first
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    if email in data[activity]["participants"]:
        # remove if present to start fresh
        client.post(f"/activities/{activity}/unregister?email={email}")

    # signup
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]

    # unregister
    resp = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]
