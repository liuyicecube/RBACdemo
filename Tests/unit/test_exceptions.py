"""Unit tests for Exceptions module"""

import pytest


class TestExceptions:
    """Test Exceptions module"""

    def test_import_exceptions(self):
        """Test that exceptions can be imported"""
        from App.Core.Exceptions import CustomException
        from App.Core.Exceptions import AuthenticationException
        from App.Core.Exceptions import PermissionException
        from App.Core.Exceptions import NotFoundException
        from App.Core.Exceptions import ValidationException
        from App.Core.Exceptions import ServerException
        from App.Core.Exceptions import TokenExpiredException
        from App.Core.Exceptions import TokenInvalidException
        from App.Core.Exceptions import UserNotFoundException
        from App.Core.Exceptions import RoleNotFoundException
        from App.Core.Exceptions import DuplicateException
        from App.Core.Exceptions import UserAlreadyExistsException
        from App.Core.Exceptions import RoleAlreadyExistsException
        from App.Core.Exceptions import RateLimitException
        from App.Core.Exceptions import DatabaseException
        from App.Core.Exceptions import CacheException

        assert CustomException is not None
        assert AuthenticationException is not None
        assert PermissionException is not None
        assert NotFoundException is not None
        assert ValidationException is not None
        assert ServerException is not None
        assert TokenExpiredException is not None
        assert TokenInvalidException is not None
        assert UserNotFoundException is not None
        assert RoleNotFoundException is not None
        assert DuplicateException is not None
        assert UserAlreadyExistsException is not None
        assert RoleAlreadyExistsException is not None
        assert RateLimitException is not None
        assert DatabaseException is not None
        assert CacheException is not None

    def test_create_authentication_exception(self):
        """Test creating AuthenticationException"""
        from App.Core.Exceptions import AuthenticationException

        exc = AuthenticationException()
        assert exc.status_code == 401
        assert exc.error_code == 40100
        assert exc.detail == "认证失败"

    def test_create_token_expired_exception(self):
        """Test creating TokenExpiredException"""
        from App.Core.Exceptions import TokenExpiredException

        exc = TokenExpiredException()
        assert exc.status_code == 401
        assert exc.error_code == 40101
        assert exc.detail == "令牌已过期"

    def test_create_token_invalid_exception(self):
        """Test creating TokenInvalidException"""
        from App.Core.Exceptions import TokenInvalidException

        exc = TokenInvalidException()
        assert exc.status_code == 401
        assert exc.error_code == 40102
        assert exc.detail == "无效的令牌"

    def test_create_permission_exception(self):
        """Test creating PermissionException"""
        from App.Core.Exceptions import PermissionException

        exc = PermissionException()
        assert exc.status_code == 403
        assert exc.error_code == 40300
        assert exc.detail == "权限不足"

    def test_create_not_found_exception(self):
        """Test creating NotFoundException"""
        from App.Core.Exceptions import NotFoundException

        exc = NotFoundException()
        assert exc.status_code == 404
        assert exc.error_code == 40400
        assert exc.detail == "资源不存在"

    def test_create_user_not_found_exception(self):
        """Test creating UserNotFoundException"""
        from App.Core.Exceptions import UserNotFoundException

        exc = UserNotFoundException()
        assert exc.status_code == 404
        assert exc.error_code == 40401
        assert exc.detail == "用户不存在"

    def test_create_role_not_found_exception(self):
        """Test creating RoleNotFoundException"""
        from App.Core.Exceptions import RoleNotFoundException

        exc = RoleNotFoundException()
        assert exc.status_code == 404
        assert exc.error_code == 40402
        assert exc.detail == "角色不存在"

    def test_create_validation_exception(self):
        """Test creating ValidationException"""
        from App.Core.Exceptions import ValidationException

        exc = ValidationException()
        assert exc.status_code == 400
        assert exc.error_code == 40000
        assert exc.detail == "数据验证失败"

    def test_create_duplicate_exception(self):
        """Test creating DuplicateException"""
        from App.Core.Exceptions import DuplicateException

        exc = DuplicateException()
        assert exc.status_code == 409
        assert exc.error_code == 40900
        assert exc.detail == "数据已存在"

    def test_create_user_already_exists_exception(self):
        """Test creating UserAlreadyExistsException"""
        from App.Core.Exceptions import UserAlreadyExistsException

        exc = UserAlreadyExistsException()
        assert exc.status_code == 409
        assert exc.error_code == 40901
        assert exc.detail == "用户已存在"

    def test_create_role_already_exists_exception(self):
        """Test creating RoleAlreadyExistsException"""
        from App.Core.Exceptions import RoleAlreadyExistsException

        exc = RoleAlreadyExistsException()
        assert exc.status_code == 409
        assert exc.error_code == 40902
        assert exc.detail == "角色已存在"

    def test_create_rate_limit_exception(self):
        """Test creating RateLimitException"""
        from App.Core.Exceptions import RateLimitException

        exc = RateLimitException()
        assert exc.status_code == 429
        assert exc.error_code == 42900
        assert exc.detail == "请求过于频繁"

    def test_create_server_exception(self):
        """Test creating ServerException"""
        from App.Core.Exceptions import ServerException

        exc = ServerException()
        assert exc.status_code == 500
        assert exc.error_code == 50000
        assert exc.detail == "服务器内部错误"

    def test_create_database_exception(self):
        """Test creating DatabaseException"""
        from App.Core.Exceptions import DatabaseException

        exc = DatabaseException()
        assert exc.status_code == 500
        assert exc.error_code == 50001
        assert exc.detail == "数据库操作失败"

    def test_create_cache_exception(self):
        """Test creating CacheException"""
        from App.Core.Exceptions import CacheException

        exc = CacheException()
        assert exc.status_code == 500
        assert exc.error_code == 50002
        assert exc.detail == "缓存操作失败"

    def test_custom_message(self):
        """Test creating exception with custom message"""
        from App.Core.Exceptions import AuthenticationException

        custom_msg = "自定义认证失败消息"
        exc = AuthenticationException(detail=custom_msg)
        assert exc.detail == custom_msg
