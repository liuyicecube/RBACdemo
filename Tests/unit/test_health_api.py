"""Unit tests for Health API module"""

import pytest


class TestHealthApi:
    """Test Health API module"""

    def test_import_health_api(self):
        """Test that Health API can be imported"""
        from App.Api.V1.Health import router
        assert router is not None
        assert hasattr(router, 'prefix')
