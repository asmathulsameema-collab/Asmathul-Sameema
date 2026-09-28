import os
os.environ["USE_MOCK_AI"] = "true"
os.environ["ADMIN_PASSWORD"] = "test-password"

from fastapi.testclient import TestClient

from app.main import app


def test_health():
    with TestClient(app) as client:
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


def test_home():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert "Create your plan" in response.text


def test_generate_plan():
    with TestClient(app) as client:
        response = client.post(
            "/generate-workout",
            data={
                "user_id": "test-user",
                "name": "Test User",
                "age": 22,
                "weight": 60,
                "goal": "general wellness",
                "intensity": "medium",
            },
        )
        assert response.status_code == 200
        assert "7-Day Workout Plan" in response.text
        assert "Test User" in response.text


def test_feedback_update():
    with TestClient(app) as client:
        client.post(
            "/generate-workout",
            data={
                "user_id": "feedback-user",
                "name": "Feedback User",
                "age": 24,
                "weight": 65,
                "goal": "general wellness",
                "intensity": "medium",
            },
        )
        response = client.post(
            "/submit-feedback",
            data={"user_id": "feedback-user", "feedback": "Add more cardio and keep sessions shorter."},
        )
        assert response.status_code == 200
        assert "Plan updated" in response.text


def test_api_user():
    with TestClient(app) as client:
        client.post(
            "/generate-workout",
            data={
                "user_id": "api-user",
                "name": "API User",
                "age": 25,
                "weight": 70,
                "goal": "muscle gain",
                "intensity": "medium",
            },
        )
        response = client.get("/api/users/api-user")
        assert response.status_code == 200
        assert response.json()["user"]["user_id"] == "api-user"


def test_admin_requires_auth():
    with TestClient(app) as client:
        response = client.get("/view-all-users")
        assert response.status_code == 401


def test_admin_dashboard():
    with TestClient(app) as client:
        response = client.get("/view-all-users", auth=("admin", "test-password"))
        assert response.status_code == 200
        assert "Users & plans" in response.text
