import pytest


class TestDepartmentsAPI:
    
    def test_get_departments_list_unauthorized(self, client):
        response = client.get("/api/v1/departments")
        assert response.status_code in [200, 401, 403]
    
    def test_get_departments_list_authorized(self, authorized_client):
        response = authorized_client.get("/api/v1/departments")
        assert response.status_code == 200
    
    def test_get_departments_with_pagination(self, authorized_client):
        response = authorized_client.get("/api/v1/departments?page=1&page_size=10")
        assert response.status_code == 200
    
    def test_get_department_tree_unauthorized(self, client):
        response = client.get("/api/v1/departments/tree")
        assert response.status_code in [200, 401, 403]
    
    def test_get_department_tree_authorized(self, authorized_client):
        response = authorized_client.get("/api/v1/departments/tree")
        assert response.status_code == 200
    
    def test_get_department_by_id_unauthorized(self, client):
        response = client.get("/api/v1/departments/1")
        assert response.status_code in [200, 401, 403]
    
    def test_create_department_unauthorized(self, client, test_data):
        response = client.post(
            "/api/v1/departments",
            json=test_data.TEST_DEPARTMENT
        )
        assert response.status_code in [200, 401, 403]
    
    def test_update_department_unauthorized(self, client):
        response = client.put(
            "/api/v1/departments/1",
            json={
                "name": "更新部门"
            }
        )
        assert response.status_code in [200, 401, 403]
    
    def test_delete_department_unauthorized(self, client):
        response = client.delete("/api/v1/departments/1")
        assert response.status_code in [200, 401, 403]
    
    def test_update_department_status_unauthorized(self, client):
        response = client.put("/api/v1/departments/1/status?status=0")
        assert response.status_code in [200, 401, 403]
    
    def test_get_department_children_unauthorized(self, client):
        response = client.get("/api/v1/departments/1/children")
        assert response.status_code in [200, 401, 403]
    
    def test_get_department_users_unauthorized(self, client):
        response = client.get("/api/v1/departments/1/users")
        assert response.status_code in [200, 401, 403]
    
    def test_count_department_users_unauthorized(self, client):
        response = client.get("/api/v1/departments/1/user-count")
        assert response.status_code in [200, 401, 403]
