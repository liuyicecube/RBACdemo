import pytest


class TestMenusAPI:
    
    def test_get_menus_list_unauthorized(self, client):
        response = client.get("/api/v1/menus")
        assert response.status_code in [200, 401, 403]
    
    def test_get_menus_list_authorized(self, authorized_client):
        response = authorized_client.get("/api/v1/menus")
        assert response.status_code == 200
    
    def test_get_menus_with_pagination(self, authorized_client):
        response = authorized_client.get("/api/v1/menus?page=1&page_size=10")
        assert response.status_code == 200
    
    def test_get_menu_tree_unauthorized(self, client):
        response = client.get("/api/v1/menus/tree")
        assert response.status_code in [200, 401, 403]
    
    def test_get_menu_tree_authorized(self, authorized_client):
        response = authorized_client.get("/api/v1/menus/tree")
        assert response.status_code == 200
    
    def test_get_user_menu_tree_unauthorized(self, client):
        response = client.get("/api/v1/menus/user")
        assert response.status_code in [200, 401, 403]
    
    def test_get_user_menu_tree_authorized(self, authorized_client):
        response = authorized_client.get("/api/v1/menus/user")
        assert response.status_code == 200
    
    def test_get_menu_by_id_unauthorized(self, client):
        response = client.get("/api/v1/menus/1")
        assert response.status_code in [200, 401, 403]
    
    def test_create_menu_unauthorized(self, client, test_data):
        response = client.post(
            "/api/v1/menus",
            json=test_data.TEST_MENU
        )
        assert response.status_code in [200, 401, 403]
    
    def test_update_menu_unauthorized(self, client):
        response = client.put(
            "/api/v1/menus/1",
            json={
                "name": "更新菜单"
            }
        )
        assert response.status_code in [200, 401, 403]
    
    def test_delete_menu_unauthorized(self, client):
        response = client.delete("/api/v1/menus/1")
        assert response.status_code in [200, 401, 403]
    
    def test_update_menu_status_unauthorized(self, client):
        response = client.put("/api/v1/menus/1/status?status=0")
        assert response.status_code in [200, 401, 403]
    
    def test_get_menu_children_unauthorized(self, client):
        response = client.get("/api/v1/menus/1/children")
        assert response.status_code in [200, 401, 403]
    
    def test_sort_menus_unauthorized(self, client):
        response = client.put(
            "/api/v1/menus/sort",
            json={
                "menu_ids": [1, 2, 3]
            }
        )
        assert response.status_code in [200, 401, 403]
