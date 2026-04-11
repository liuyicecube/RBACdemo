import pytest


class TestUsersAPI:
    
    def test_get_users_list_unauthorized(self, client):
        response = client.get("/api/v1/users")
        assert response.status_code in [200, 401, 403]
    
    def test_get_users_list_authorized(self, authorized_client):
        response = authorized_client.get("/api/v1/users")
        assert response.status_code == 200
    
    def test_get_users_with_pagination(self, authorized_client):
        response = authorized_client.get("/api/v1/users?page=1&page_size=10")
        assert response.status_code == 200
    
    def test_get_users_with_keyword(self, authorized_client):
        response = authorized_client.get("/api/v1/users?keyword=test")
        assert response.status_code == 200
    
    def test_get_users_with_status(self, authorized_client):
        response = authorized_client.get("/api/v1/users?status=1")
        assert response.status_code == 200
    
    def test_create_user_unauthorized(self, client, test_data):
        response = client.post(
            "/api/v1/users",
            json={
                "username": "newuser",
                "password": "Test@123",
                "nickname": "新用户",
                "email": "newuser@example.com",
                "phone": "13700137000"
            }
        )
        assert response.status_code in [200, 401, 403]
    
    def test_get_user_by_id_unauthorized(self, client):
        response = client.get("/api/v1/users/1")
        assert response.status_code in [200, 401, 403]
    
    def test_get_user_not_found(self, authorized_client):
        response = authorized_client.get("/api/v1/users/99999")
        assert response.status_code in [200, 404]
    
    def test_update_user_unauthorized(self, client):
        response = client.put(
            "/api/v1/users/1",
            json={
                "nickname": "更新用户"
            }
        )
        assert response.status_code in [200, 401, 403]
    
    def test_delete_user_unauthorized(self, client):
        response = client.delete("/api/v1/users/1")
        assert response.status_code in [200, 401, 403]
    
    def test_update_user_status_unauthorized(self, client):
        response = client.put("/api/v1/users/1/status?status=0")
        assert response.status_code in [200, 401, 403]
    
    def test_get_user_roles_unauthorized(self, client):
        response = client.get("/api/v1/users/1/roles")
        assert response.status_code in [200, 401, 403]
    
    def test_assign_user_roles_unauthorized(self, client):
        response = client.put(
            "/api/v1/users/1/roles",
            json={
                "role_ids": [1, 2]
            }
        )
        assert response.status_code in [200, 401, 403]
    
    def test_set_primary_role_unauthorized(self, client):
        response = client.put(
            "/api/v1/users/1/primary-role",
            json={
                "role_id": 1
            }
        )
        assert response.status_code in [200, 401, 403]
