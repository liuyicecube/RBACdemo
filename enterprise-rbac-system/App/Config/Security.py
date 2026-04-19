"""Security Configuration"""

from passlib.context import CryptContext
from App.Config.Settings import settings


# 创建密码上下文
pwd_context = CryptContext(
    schemes=["bcrypt"],
    bcrypt__default_rounds=settings.bcrypt_rounds,
    bcrypt__ident="2b"  # 使用b2版本的bcrypt算法
)


class SecurityConfig:
    """Security configuration"""

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except (ValueError, TypeError):
            return False

    @staticmethod
    def get_password_hash(password: str) -> str:
        """获取密码哈希值"""
        return pwd_context.hash(password)

    @staticmethod
    def generate_salt(length: int = 16) -> str:
        """生成随机盐值（保留方法但不使用）"""
        import secrets
        return secrets.token_hex(length)
