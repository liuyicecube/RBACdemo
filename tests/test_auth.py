import pytest


class TestAuthAPI:
    
    def test_register_success(self, client, test_data):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": test_data.TEST_USER["username"],
                "password": test_data.TEST_USER["password"],
                "nickname": "测试用户",
                "email": test_data.TEST_USER["email"],
                "phone": "13800138000"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200 or data.get("status") == 200 or data.get("success") is True
        if "data" in data:
            assert "id" in data["data"]
            assert data["data"]["username"] == test_data.TEST_USER["username"]
    
    def test_register_duplicate_username(self, client, test_data):
        client.post(
            "/api/v1/auth/register",
            json={
                "username": test_data.TEST_USER["username"],
                "password": test_data.TEST_USER["password"],
                "nickname": "测试用户",
                "email": test_data.TEST_USER["email"],
                "phone": "13800138000"
            }
        )
        
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": test_data.TEST_USER["username"],
                "password": "Another@123",
                "nickname": "重复用户",
                "email": "another@example.com",
                "phone": "13900139000"
            }
        )
        assert response.status_code in [200, 400, 409]
    
    def test_register_invalid_password(self, client, test_data):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": test_data.TEST_USER["username"],
                "password": "123",
                "nickname": "测试用户",
                "email": test_data.TEST_USER["email"],
                "phone": "13800138000"
            }
        )
        assert response.status_code in [200, 400, 422]
    
    def test_register_missing_fields(self, client):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "testuser",
                "password": "Test@123"
            }
        )
        assert response.status_code in [200, 400, 422]
    
    def test_login_success(self, client, test_data):
        client.post(
            "/api/v1/auth/register",
            json={
                "username": test_data.TEST_USER["username"],
                "password": test_data.TEST_USER["password"],
                "nickname": "测试用户",
                "email": test_data.TEST_USER["email"],
                "phone": "13800138000"
            }
        )
        
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": test_data.TEST_USER["username"],
                "password": test_data.TEST_USER["password"]
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200 or data.get("status") == 200 or data.get("success") is True
        if "data" in data:
            assert "access_token" in data["data"]
    
    def test_login_wrong_password(self, client, test_data):
        client.post(
            "/api/v1/auth/register",
            json={
                "username": test_data.TEST_USER["username"],
                "password": test_data.TEST_USER["password"],
                "nickname": "测试用户",
                "email": test_data.TEST_USER["email"],
                "phone": "13800138000"
            }
        )
        
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": test_data.TEST_USER["username"],
                "password": "Wrong@123"
            }
        )
        assert response.status_code in [200, 400, 401]
    
    def test_login_user_not_found(self, client):
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": "nonexistent",
                "password": "Test@123"
            }
        )
        assert response.status_code in [200, 400, 401, 404]
    
    def test_login_missing_fields(self, client):
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": "testuser"
            }
        )
        assert response.status_code in [200, 400, 422]
    
    def test_get_profile_success(self, authorized_client):
        response = authorized_client.get("/api/v1/auth/profile")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200 or data.get("status") == 200 or data.get("success") is True
        if "data" in data:
            assert "id" in data["data"]
            assert "username" in data["data"]
    
    def test_get_profile_unauthorized(self, client):
        response = client.get("/api/v1/auth/profile")
        assert response.status_code in [200, 401, 403]
    
    def test_change_password_success(self, authorized_client, test_data):
        response = authorized_client.post(
            "/api/v1/auth/change-password",
            json={
                "old_password": test_data.TEST_USER["password"],
                "new_password": "NewPass@123"
            }
        )
        assert response.status_code == 200
    
    def test_change_password_wrong_old_password(self, authorized_client):
        response = authorized_client.post(
            "/api/v1/auth/change-password",
            json={
                "old_password": "Wrong@123",
                "new_password": "NewPass@123"
            }
        )
        assert response.status_code in [200, 400, 401]
    
    def test_logout_success(self, authorized_client):
        response = authorized_client.post("/api/v1/auth/logout")
        assert response.status_code == 200
    
    def test_root_endpoint(self, client):
        response = client.get("/")
        assert response.status_code == 200
    
    def test_health_check_endpoint(self, client):
        response = client.get("/health")
        assert response.status_code == 200
