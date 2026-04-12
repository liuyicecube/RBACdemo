"""Application Settings"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # 应用配置
    app_name: str = "Enterprise RBAC System"
    app_version: str = "1.0.0"
    app_debug: bool = True

    # 数据库配置
    database_url: str = "mysql+pymysql://root:1124@192.168.99.220:3306/lydata?charset=utf8mb4"

    # JWT配置
    jwt_secret_key: str = "your-secret-key-here"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # Redis配置
    redis_url: str = "redis://localhost:6379/0"

    # Redis Sentinel配置（可选）
    redis_sentinel_urls: Optional[str] = None
    redis_sentinel_master_name: Optional[str] = None

    # 安全配置
    password_salt_length: int = 16
    bcrypt_rounds: int = 12

    # 上传配置
    upload_dir: str = "./uploads"
    max_file_size: int = 5242880  # 5MB
    allowed_image_extensions: str = "png,jpg,jpeg,gif"

    # CORS配置
    cors_origins: str = "http://localhost:3000,http://localhost:8080,http://localhost:5175"

    # 日志配置
    log_level: str = "INFO"
    log_dir: str = "./Logs"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__"
    )


# 创建全局设置实例
settings = Settings()
