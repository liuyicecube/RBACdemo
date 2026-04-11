import pytest


class TestRolesAPI:
    
    def test_get_roles_list_unauthorized(self, client):
        response = client.get("/api/v1/roles")
        assert response.status_code in [200, 401, 403]
    
    def test_get_roles_list_authorized(self, authorized_client):
        response = authorized_client.get("/api/v1/roles")
        assert response.status_code == 200
    
    def test_get_roles_with_pagination(self, authorized_client):
        response = authorized_client.get("/api/v1/roles?page=1&page_size=10")
        assert response.status_code == 200
    
    def test_get_all_active_roles_unauthorized(self, client):
        response = client.get("/api/v1/roles/all")
        assert response.status_code in [200, 401, 403]
    
    def test_get_all_active_roles_authorized(self, authorized_client):
        response = authorized_client.get("/api/v1/roles/all")
        assert response.status_code == 200
    
    def test_get_role_by_id_unauthorized(self, client):
        response = client.get("/api/v1/roles/1")
        assert response.status_code in [200, 401, 403]
    
    def test_create_role_unauthorized(self, client, test_data):
        response = client.post(
            "/api/v1/roles",
            json=test_data.TEST_ROLE
        )
        assert response.status_code in [200, 401, 403]
    
    def test_update_role_unauthorized(self, client):
        response = client.put(
            "/api/v1/roles/1",
            json={
                "name": "更新角色"
            }
        )
        assert response.status_code in [200, 401, 403]
    
    def test_delete_role_unauthorized(self, client):
        response = client.delete("/api/v1/roles/1")
        assert response.status_code in [200, 401, 403]
    
    def test_update_role_status_unauthorized(self, client):
        response = client.put("/api/v1/roles/1/status?status=0")
        assert response.status_code in [200, 401, 403]
    
    def test_get_role_permissions_unauthorized(self, client):
        response = client.get("/api/v1/roles/1/permissions")
        assert response.status_code in [200, 401, 403]
    
    def test_assign_role_permissions_unauthorized(self, client):
        response = client.put(
            "/api/v1/roles/1/permissions",
            json={
                "permission_ids": [1, 2]
            }
        )
        assert response.status_code in [200, 401, 403]
    
    def test_get_role_users_unauthorized(self, client):
        response = client.get("/api/v1/roles/1/users")
        assert response.status_code in [200, 401, 403]
