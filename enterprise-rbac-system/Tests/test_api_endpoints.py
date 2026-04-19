"""测试所有API端点"""
import pytest
from fastapi.testclient import TestClient

class TestAPIEndpoints:
    """测试所有API端点的存在性"""
    
    @pytest.mark.parametrize("endpoint", [
        "/api/v1/users",
        "/api/v1/roles",
        "/api/v1/permissions",
        "/api/v1/menus",
        "/api/v1/departments",
        "/api/v1/user-groups",
        "/api/v1/data-permission-rules",
        "/api/v1/system-dicts",
        "/api/v1/system-configs",
        "/api/v1/operation-logs",
        "/api/v1/audit-logs",
        "/api/v1/user-sessions",
        "/api/v1/dashboard",
        "/api/v1/metrics",
        "/api/v1/health",
    ])
    def test_endpoint_exists(self, client: TestClient, endpoint: str):
        """测试端点存在（返回不是404）"""
        response = client.get(endpoint)
        # 需要认证的端点返回401是正常的，404表示不存在
        assert response.status_code != 404
