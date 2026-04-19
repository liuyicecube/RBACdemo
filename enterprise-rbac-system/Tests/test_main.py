"""测试主应用"""
import pytest
from fastapi.testclient import TestClient

class TestMainEndpoints:
    """测试主应用端点"""
    
    def test_root_endpoint(self, client: TestClient):
        """测试根路径"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "app_name" in data["data"]
        assert "version" in data["data"]
        assert data["data"]["status"] == "running"
    
    def test_health_check(self, client: TestClient):
        """测试健康检查"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["status"] == "healthy"
    
    def test_api_docs(self, client: TestClient):
        """测试API文档"""
        response = client.get("/docs")
        assert response.status_code == 200
        
        response = client.get("/redoc")
        assert response.status_code == 200
        
        response = client.get("/openapi.json")
        assert response.status_code == 200
