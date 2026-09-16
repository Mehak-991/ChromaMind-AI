import pytest


@pytest.mark.asyncio
async def test_register_and_login_flow(db_session, async_client):
    # 1. Register a new user
    user_data = {
        "email": "test_auth_user@chromamind.ai",
        "full_name": "Test Auth User",
        "password": "securepassword123",
    }
    response = await async_client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "id" in data

    # 2. Try registering same email (duplicate)
    dup_response = await async_client.post("/api/v1/auth/register", json=user_data)
    assert dup_response.status_code == 400

    # 3. Login with wrong password
    wrong_login = {"email": "test_auth_user@chromamind.ai", "password": "wrongpassword"}
    wrong_response = await async_client.post("/api/v1/auth/login", json=wrong_login)
    assert wrong_response.status_code == 400

    # 4. Login with correct password
    login_data = {
        "email": "test_auth_user@chromamind.ai",
        "password": "securepassword123",
    }
    login_response = await async_client.post("/api/v1/auth/login", json=login_data)
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    assert token_data["user"]["email"] == user_data["email"]

    # 5. Access protected route with missing token
    protected_resp_missing = await async_client.patch(
        "/api/v1/settings",
        json={
            "default_delta_e_threshold": 1.5,
            "optimizer_max_iterations": 1000,
            "enable_explainability": True,
        },
    )
    assert protected_resp_missing.status_code == 401

    # 6. Access protected route with valid token
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    protected_resp_valid = await async_client.patch(
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
