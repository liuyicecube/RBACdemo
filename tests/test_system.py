import pytest


class TestSystemDictsAPI:
    
    def test_get_system_dicts_list_unauthorized(self, client):
        response = client.get("/api/v1/system-dicts")
        assert response.status_code in [200, 401, 403]
    
    def test_get_system_dicts_list_authorized(self, authorized_client):
        response = authorized_client.get("/api/v1/system-dicts")
        assert response.status_code == 200


class TestSystemConfigsAPI:
    
    def test_get_system_configs_list_unauthorized(self, client):
        response = client.get("/api/v1/system-configs")
        assert response.status_code in [200, 401, 403]
    
    def test_get_system_configs_list_authorized(self, authorized_client):
        response = authorized_client.get("/api/v1/system-configs")
        assert response.status_code == 200


class TestOperationLogsAPI:
    
    def test_get_operation_logs_list_unauthorized(self, client):
        response = client.get("/api/v1/operation-logs")
        assert response.status_code in [200, 401, 403]
    
    def test_get_operation_logs_list_authorized(self, authorized_client):
        response = authorized_client.get("/api/v1/operation-logs")
        assert response.status_code == 200


class TestAuditLogsAPI:
    
    def test_get_audit_logs_list_unauthorized(self, client):
        response = client.get("/api/v1/audit-logs")
        assert response.status_code in [200, 401, 403]
    
    def test_get_audit_logs_list_authorized(self, authorized_client):
        response = authorized_client.get("/api/v1/audit-logs")
        assert response.status_code == 200


class TestUserGroupsAPI:
    
    def test_get_user_groups_list_unauthorized(self, client):
        response = client.get("/api/v1/user-groups")
        assert response.status_code in [200, 401, 403]
    
    def test_get_user_groups_list_authorized(self, authorized_client):
        response = authorized_client.get("/api/v1/user-groups")
        assert response.status_code == 200


class TestDataPermissionRulesAPI:
    
    def test_get_data_permission_rules_list_unauthorized(self, client):
        response = client.get("/api/v1/data-permission-rules")
        assert response.status_code in [200, 401, 403]
    
    def test_get_data_permission_rules_list_authorized(self, authorized_client):
        response = authorized_client.get("/api/v1/data-permission-rules")
        assert response.status_code == 200


class TestUserSessionsAPI:
    
    def test_get_user_sessions_list_unauthorized(self, client):
        response = client.get("/api/v1/user-sessions")
        assert response.status_code in [200, 401, 403]
    
    def test_get_user_sessions_list_authorized(self, authorized_client):
        response = authorized_client.get("/api/v1/user-sessions")
        assert response.status_code == 200


class TestUserProfilesAPI:
    
    def test_get_user_profiles_list_unauthorized(self, client):
        response = client.get("/api/v1/user-profiles")
        assert response.status_code in [200, 401, 403]
    
    def test_get_user_profiles_list_authorized(self, authorized_client):
        response = authorized_client.get("/api/v1/user-profiles")
        assert response.status_code == 200


class TestMetricsAPI:
    
    def test_get_metrics_unauthorized(self, client):
        response = client.get("/api/v1/metrics")
        assert response.status_code in [200, 401, 403]
    
    def test_get_metrics_authorized(self, authorized_client):
        response = authorized_client.get("/api/v1/metrics")
        assert response.status_code == 200
