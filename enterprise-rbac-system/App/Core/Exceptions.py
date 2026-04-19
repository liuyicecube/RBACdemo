"""Custom Exceptions"""

from fastapi import HTTPException, status
from typing import Optional, Dict, Any


class CustomException(HTTPException):
    """自定义异常基类"""

    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: int,
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code


class AuthenticationException(CustomException):
    """认证异常"""

    def __init__(self, detail: str = "认证失败", error_code: int = 40100):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code=error_code
        )


class TokenExpiredException(AuthenticationException):
    """令牌过期异常"""

    def __init__(self, detail: str = "令牌已过期", error_code: int = 40101):
        super().__init__(detail=detail, error_code=error_code)


class TokenInvalidException(AuthenticationException):
    """令牌无效异常"""

    def __init__(self, detail: str = "无效的令牌", error_code: int = 40102):
        super().__init__(detail=detail, error_code=error_code)


class PermissionException(CustomException):
    """权限异常"""

    def __init__(self, detail: str = "权限不足", error_code: int = 40300):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code=error_code
        )


class NotFoundException(CustomException):
    """资源不存在异常"""

    def __init__(self, detail: str = "资源不存在", error_code: int = 40400):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code=error_code
        )


class UserNotFoundException(NotFoundException):
    """用户不存在异常"""

    def __init__(self, detail: str = "用户不存在", error_code: int = 40401):
        super().__init__(detail=detail, error_code=error_code)


class RoleNotFoundException(NotFoundException):
    """角色不存在异常"""

    def __init__(self, detail: str = "角色不存在", error_code: int = 40402):
        super().__init__(detail=detail, error_code=error_code)


class ValidationException(CustomException):
    """数据验证异常"""

    def __init__(self, detail: str = "数据验证失败", error_code: int = 40000):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code=error_code
        )


class DuplicateException(CustomException):
    """重复数据异常"""

    def __init__(self, detail: str = "数据已存在", error_code: int = 40900):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code=error_code
        )


class UserAlreadyExistsException(DuplicateException):
    """用户已存在异常"""

    def __init__(self, detail: str = "用户已存在", error_code: int = 40901):
        super().__init__(detail=detail, error_code=error_code)


class RoleAlreadyExistsException(DuplicateException):
    """角色已存在异常"""

    def __init__(self, detail: str = "角色已存在", error_code: int = 40902):
        super().__init__(detail=detail, error_code=error_code)


class RateLimitException(CustomException):
    """限流异常"""

    def __init__(self, detail: str = "请求过于频繁", error_code: int = 42900):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            error_code=error_code
        )


class ServerException(CustomException):
    """服务器内部异常"""

    def __init__(self, detail: str = "服务器内部错误", error_code: int = 50000):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code=error_code
        )


class DatabaseException(ServerException):
    """数据库异常"""

    def __init__(self, detail: str = "数据库操作失败", error_code: int = 50001):
        super().__init__(detail=detail, error_code=error_code)


class CacheException(ServerException):
    """缓存异常"""

    def __init__(self, detail: str = "缓存操作失败", error_code: int = 50002):
        super().__init__(detail=detail, error_code=error_code)
