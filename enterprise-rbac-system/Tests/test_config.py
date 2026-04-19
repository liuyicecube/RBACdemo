"""测试配置"""
import pytest
from App.Config.Settings import settings

class TestSettings:
    """测试应用配置"""
    
    def test_required_settings(self):
        """测试必需的配置项"""
        assert settings.app_name is not None
        assert settings.app_version is not None
        assert settings.database_url is not None
        assert settings.jwt_secret_key is not None
        assert settings.jwt_algorithm is not None
    
    def test_jwt_settings(self):
        """测试JWT配置"""
        assert settings.jwt_access_token_expire_minutes > 0
        assert settings.jwt_refresh_token_expire_days > 0
    
    def test_security_settings(self):
        """测试安全配置"""
        assert settings.password_salt_length >= 8
        assert settings.bcrypt_rounds >= 10
    
    def test_upload_settings(self):
        """测试上传配置"""
        assert settings.upload_dir is not None
        assert settings.max_file_size > 0
        assert len(settings.allowed_image_extensions) > 0
    
    def test_cors_settings(self):
        """测试CORS配置"""
        assert settings.cors_origins is not None
        assert isinstance(settings.cors_origins, list)
