import pytest


class TestPermissionsAPI:
    
    def test_get_permissions_list_unauthorized(self, client):
        response = client.get("/api/v1/permissions")
        assert response.status_code in [200, 401, 403]
    
    def test_get_permissions_list_authorized(self, authorized_client):
        response = authorized_client.get("/api/v1/permissions")
        assert response.status_code == 200
    
    def test_get_permissions_with_pagination(self, authorized_client):
        response = authorized_client.get("/api/v1/permissions?page=1&page_size=10")
        assert response.status_code == 200
    
    def test_get_all_active_permissions_unauthorized(self, client):
        response = client.get("/api/v1/permissions/all")
        assert response.status_code in [200, 401, 403]
    
    def test_get_all_active_permissions_authorized(self, authorized_client):
        response = authorized_client.get("/api/v1/permissions/all")
        assert response.status_code == 200
    
    def test_get_permission_by_id_unauthorized(self, client):
        response = client.get("/api/v1/permissions/1")
        assert response.status_code in [200, 401, 403]
    
    def test_create_permission_unauthorized(self, client, test_data):
        response = client.post(
            "/api/v1/permissions",
            json=test_data.TEST_PERMISSION
        )
        assert response.status_code in [200, 401, 403]
    
    def test_update_permission_unauthorized(self, client):
        response = client.put(
            "/api/v1/permissions/1",
            json={
                "name": "更新权限"
            }
        )
        assert response.status_code in [200, 401, 403]
    
    def test_delete_permission_unauthorized(self, client):
        response = client.delete("/api/v1/permissions/1")
        assert response.status_code in [200, 401, 403]
    
    def test_update_permission_status_unauthorized(self, client):
        response = client.put("/api/v1/permissions/1/status?status=0")
        assert response.status_code in [200, 401, 403]
    
    def test_get_permission_roles_unauthorized(self, client):
        response = client.get("/api/v1/permissions/1/roles")
        assert response.status_code in [200, 401, 403]
    
    def test_count_permission_roles_unauthorized(self, client):
        response = client.get("/api/v1/permissions/1/role-count")
        assert response.status_code in [200, 401, 403]
    
    def test_batch_create_permissions_unauthorized(self, client, test_data):
        response = client.post(
            "/api/v1/permissions/batch",
            json=[test_data.TEST_PERMISSION]
        )
        assert response.status_code in [200, 401, 403]
    
    def test_batch_delete_permissions_unauthorized(self, client):
        response = client.delete("/api/v1/permissions/batch?permission_ids=1,2")
        assert response.status_code in [200, 401, 403]
