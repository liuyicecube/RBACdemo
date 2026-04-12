"""Unit tests for security module"""

import pytest


class TestSecurityCore:
    """Test SecurityCore"""

    def test_import_security_core(self):
        """Test that SecurityCore can be imported"""
        from App.Core.Security import SecurityCore
        assert SecurityCore is not None

    def test_password_hashing(self):
        """Test password hashing functionality"""
        from App.Core.Security import SecurityCore
        
        password = "test_password_123"
        hashed = SecurityCore.hash_password(password)
        
        assert hashed is not None
        assert hashed != password
        assert SecurityCore.verify_password(password, hashed) is True
        assert SecurityCore.verify_password("wrong_password", hashed) is False
