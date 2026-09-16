import uuid
from datetime import datetime
from pathlib import Path
import sys
from unittest.mock import patch

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.api.deps import get_current_user
from app.api.v1.routes import get_settings_repo, get_user_repo
from app.main import app
from app.models.models import User, UserSettings


class InMemoryUserRepo:
    def __init__(self):
        self._users_by_email = {}

    async def get_by_email(self, email: str):
        return self._users_by_email.get(email)

    async def create(self, user: User):
        if user.id is None:
            user.id = uuid.uuid4()
        if user.is_active is None:
            user.is_active = True
        if user.created_at is None:
            user.created_at = datetime.utcnow()
        self._users_by_email[user.email] = user
        return user


class InMemorySettingsRepo:
    def __init__(self):
        self._settings_by_user_id = {}

    async def get_by_user_id(self, user_id):
        return self._settings_by_user_id.get(user_id)

    async def update(self, settings_obj: UserSettings):
        if settings_obj.id is None:
            settings_obj.id = uuid.uuid4()
        self._settings_by_user_id[settings_obj.user_id] = settings_obj
        return settings_obj


def test_register_and_login_flow():
    user_repo = InMemoryUserRepo()
    settings_repo = InMemorySettingsRepo()

    app.dependency_overrides[get_user_repo] = lambda: user_repo
    app.dependency_overrides[get_settings_repo] = lambda: settings_repo

    client = TestClient(app)

    with (
        patch("app.api.v1.routes.get_password_hash", lambda password: f"hashed:{password}"),
        patch(
            "app.api.v1.routes.verify_password",
            lambda password, password_hash: password_hash == f"hashed:{password}",
        ),
    ):
        # 1. Register a new user
        user_data = {
            "email": "test_auth_user@chromamind.ai",
            "full_name": "Test Auth User",
            "password": "securepassword123",
        }
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert "id" in data

        # 2. Try registering same email (duplicate)
        dup_response = client.post("/api/v1/auth/register", json=user_data)
        assert dup_response.status_code == 400

        # 3. Login with wrong password
        wrong_login = {
            "email": "test_auth_user@chromamind.ai",
            "password": "wrongpassword",
        }
        wrong_response = client.post("/api/v1/auth/login", json=wrong_login)
        assert wrong_response.status_code == 400

        # 4. Login with correct password
        login_data = {
            "email": "test_auth_user@chromamind.ai",
            "password": "securepassword123",
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        token_data = login_response.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"
        assert token_data["user"]["email"] == user_data["email"]

    # 5. Access protected route with missing token
    protected_resp_missing = client.patch(
        "/api/v1/settings",
        json={
            "default_delta_e_threshold": 1.5,
            "optimizer_max_iterations": 1000,
            "enable_explainability": True,
        },
    )
    assert protected_resp_missing.status_code == 401

    # 6. Access protected route with valid token
    current_user = User(
        id=uuid.UUID(data["id"]),
        email=user_data["email"],
        password_hash=user_repo._users_by_email[user_data["email"]].password_hash,
        full_name=user_data["full_name"],
        is_active=True,
        role="user",
        created_at=datetime.utcnow(),
    )
    app.dependency_overrides[get_current_user] = lambda: current_user

    headers = {"Authorization": "Bearer " + token_data["access_token"]}
    protected_resp_valid = client.patch(
        "/api/v1/settings",
        json={
            "default_delta_e_threshold": 1.5,
            "optimizer_max_iterations": 1000,
            "enable_explainability": True,
        },
        headers=headers,
    )
    assert protected_resp_valid.status_code == 200
    assert protected_resp_valid.json()["default_delta_e_threshold"] == 1.5
    client.close()

    app.dependency_overrides.clear()
