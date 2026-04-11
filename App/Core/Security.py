"""Security Core"""

from datetime import datetime, timedelta, UTC
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from App.Config.Settings import settings
from App.Config.Security import SecurityConfig


class SecurityCore:
    """安全核心功能"""
    
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """创建访问令牌"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(minutes=settings.jwt_access_token_expire_minutes)
        
        to_encode.update({"exp": expire, "token_type": "access"})
        encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """创建刷新令牌"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(days=settings.jwt_refresh_token_expire_days)
        
        to_encode.update({"exp": expire, "token_type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """验证令牌"""
        try:
            payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
            return payload
        except JWTError:
            return None
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """获取密码哈希值"""
        return SecurityConfig.get_password_hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return SecurityConfig.verify_password(plain_password, hashed_password)
    
    @staticmethod
    def generate_salt(length: int = 16) -> str:
        """生成随机盐值"""
        return SecurityConfig.generate_salt(length)