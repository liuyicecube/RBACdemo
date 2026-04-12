"""Unit tests for MetricsService"""

import pytest


class TestMetricsService:
    """Test MetricsService"""

    def test_import_metrics_service(self):
        """Test that MetricsService can be imported"""
        from App.Services.MetricsService import MetricsService
        assert MetricsService is not None

    def test_create_metrics_service(self):
        """Test creating MetricsService instance"""
        from App.Services.MetricsService import MetricsService
        
        service = MetricsService()
        assert service is not None
        assert hasattr(service, 'cache')

    def test_get_cache_metrics(self):
        """Test get_cache_metrics method"""
        from App.Services.MetricsService import MetricsService
        
        service = MetricsService()
        metrics = service.get_cache_metrics()
        
        assert metrics is not None
        assert isinstance(metrics, dict)

    def test_reset_cache_metrics(self):
        """Test reset_cache_metrics method"""
        from App.Services.MetricsService import MetricsService
        
        service = MetricsService()
        service.reset_cache_metrics()
        
        assert service.cache.hit_count == 0
        assert service.cache.miss_count == 0
