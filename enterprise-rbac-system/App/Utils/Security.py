"""Security Utils"""

import base64
import binascii
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from jose import JWTError, jwt
from cryptography.fernet import Fernet, InvalidToken
from App.Config.Settings import settings


class SecurityUtils:
    """安全工具类"""

    # 密码上下文
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return SecurityUtils.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """获取密码哈希"""
        return SecurityUtils.pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """创建访问令牌"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=settings.jwt_access_token_expire_minutes)
        to_encode.update({"exp": expire, "token_type": "access"})
        encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """创建刷新令牌"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(days=settings.jwt_refresh_token_expire_days)
        to_encode.update({"exp": expire, "token_type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> Optional[Dict[str, Any]]:
        """解码令牌"""
        try:
            payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
            return payload
        except JWTError:
            return None

    @staticmethod
    def _get_fernet_key() -> bytes:
        """获取Fernet密钥（从JWT密钥派生）"""
        key = settings.jwt_secret_key.encode()
        key_hash = hashlib.sha256(key).digest()
        return base64.urlsafe_b64encode(key_hash)

    @staticmethod
    def encrypt_sensitive_data(data: str) -> str:
        """加密敏感数据"""
        if not data:
            return data
        try:
            fernet = Fernet(SecurityUtils._get_fernet_key())
            encrypted = fernet.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted).decode()
        except (InvalidToken, TypeError, ValueError):
            return data

    @staticmethod
    def decrypt_sensitive_data(encrypted_data: str) -> str:
        """解密敏感数据"""
        if not encrypted_data:
            return encrypted_data
        try:
            fernet = Fernet(SecurityUtils._get_fernet_key())
            decoded = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = fernet.decrypt(decoded)
            return decrypted.decode()
        except (InvalidToken, TypeError, ValueError, binascii.Error):
            return encrypted_data
