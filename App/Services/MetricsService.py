"""Metrics Service"""

from typing import Dict, Any
from App.Utils.Cache import cache
from App.Utils.Logger import logger


class MetricsService:
    """监控指标服务类"""

    def __init__(self):
        """初始化监控指标服务"""
        self.cache = cache

    def get_cache_metrics(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        stats = self.cache.get_stats()
        logger.debug("获取缓存统计信息成功")
        return stats

    def reset_cache_metrics(self) -> None:
        """重置缓存统计信息"""
        self.cache.hit_count = 0
        self.cache.miss_count = 0
        logger.info("缓存统计信息已重置")
