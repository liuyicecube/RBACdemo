"""测试认证API"""
import pytest
from fastapi.testclient import TestClient

class TestAuthAPI:
    """测试认证相关API"""
    
    def test_login_endpoint_exists(self, client: TestClient):
        """测试登录端点存在"""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "test", "password": "test"}
        )
        # 即使认证失败，端点也应该返回401或其他状态码，而不是404
        assert response.status_code != 404
    
    def test_refresh_token_endpoint_exists(self, client: TestClient):
        """测试刷新Token端点存在"""
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "test"}
        )
        assert response.status_code != 404
    
    def test_logout_endpoint_exists(self, client: TestClient):
        """测试登出端点存在"""
        response = client.post("/api/v1/auth/logout")
        assert response.status_code != 404
