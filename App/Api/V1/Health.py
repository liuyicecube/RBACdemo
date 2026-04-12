"""Health API Router"""

from fastapi import APIRouter
from App.Core.Database import DatabaseCore
from App.Utils.Response import ResponseUtils


router = APIRouter(prefix="/health", tags=["健康检查"])


@router.get("", summary="系统健康检查")
def health_check():
    """
    系统健康检查接口
    
    返回：
    - 系统状态
    - 数据库健康状态
    - 响应时间
    """
    db_health = DatabaseCore.health_check()
    
    return ResponseUtils.success(
        data={
            "status": "ok" if db_health["status"] == "healthy" else "degraded",
            "database": db_health
        },
        message="系统健康检查完成"
    )


@router.get("/database", summary="数据库健康检查")
def database_health():
    """
    数据库健康检查接口
    
    返回：
    - 数据库状态
    - 延迟
    - 检查时间
    """
    db_health = DatabaseCore.health_check()
    
    return ResponseUtils.success(
        data=db_health,
        message="数据库健康检查完成"
    )


@router.get("/database/info", summary="数据库信息")
def database_info():
    """
    获取数据库信息接口
    
    返回：
    - 数据库版本
    - 检查时间
    """
    db_info = DatabaseCore.get_connection_info()
    
    return ResponseUtils.success(
        data=db_info,
        message="获取数据库信息成功"
    )
