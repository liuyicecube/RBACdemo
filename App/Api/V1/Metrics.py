"""Metrics API Router"""

from fastapi import APIRouter, Depends
from App.Dependencies.Auth import get_current_user
from App.Utils.Cache import cache
from App.Utils.Response import ResponseUtils


# 创建路由实例
router = APIRouter(prefix="/metrics", tags=["监控"])


@router.get("/cache", summary="获取缓存统计信息")
def get_cache_metrics(current_user: dict = Depends(get_current_user)):
    """
    获取缓存统计信息，包括命中率、请求数等
    
    - **current_user**: 当前登录用户（自动注入）
    
    返回：
    - **hit_count**: 缓存命中次数
    - **miss_count**: 缓存未命中次数
    - **total_requests**: 总请求次数
    - **hit_rate**: 缓存命中率（百分比）
    """
    return ResponseUtils.success(data=cache.get_stats(), message="获取缓存统计信息成功")


@router.get("/cache/reset", summary="重置缓存统计信息")
def reset_cache_metrics(current_user: dict = Depends(get_current_user)):
    """
    重置缓存统计信息
    
    - **current_user**: 当前登录用户（自动注入）
    
    返回：
    - **message**: 操作结果消息
    """
    # 重置缓存统计信息
    cache.hit_count = 0
    cache.miss_count = 0
    return ResponseUtils.success(message="缓存统计信息已重置")
