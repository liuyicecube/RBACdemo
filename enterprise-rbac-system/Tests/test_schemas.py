"""测试Schema验证"""
import pytest
from pydantic import ValidationError
from App.Schemas.User import UserCreate, UserUpdate
from App.Schemas.Auth import LoginRequest
from App.Schemas.Role import RoleCreate

class TestUserSchemas:
    """测试用户Schema"""
    
    def test_user_create_valid(self):
        """测试有效用户创建"""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "Password123!",
        }
        user = UserCreate(**user_data)
        assert user.username == "testuser"
        assert user.email == "test@example.com"
    
    def test_user_create_invalid_email(self):
        """测试无效邮箱"""
        user_data = {
            "username": "testuser",
            "email": "invalid-email",
            "password": "Password123!",
        }
        with pytest.raises(ValidationError):
            UserCreate(**user_data)
    
    def test_user_update_valid(self):
        """测试用户更新"""
        update_data = {"email": "new@example.com"}
        update = UserUpdate(**update_data)
        assert update.email == "new@example.com"

class TestAuthSchemas:
    """测试认证Schema"""
    
    def test_login_request_valid(self):
        """测试登录请求"""
        login_data = {
            "username": "testuser",
            "password": "Password123!"
        }
        login = LoginRequest(**login_data)
        assert login.username == "testuser"
        assert login.password == "Password123!"

class TestRoleSchemas:
    """测试角色Schema"""
    
    def test_role_create_valid(self):
        """测试角色创建"""
        role_data = {
            "name": "admin",
            "description": "Administrator role",
            "code": "ADMIN"
        }
        role = RoleCreate(**role_data)
        assert role.name == "admin"
        assert role.code == "ADMIN"
