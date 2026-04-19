"""Dashboard API Router"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from App.Dependencies.Auth import get_current_user
from App.Dependencies.Database import get_db
from App.Services.DashboardService import DashboardService
from App.Utils.Response import ResponseUtils
from App.Models.User import UserModel


# 创建路由实例
router = APIRouter(prefix="/dashboard", tags=["仪表盘"])


@router.get("/stats", summary="获取仪表盘统计数据")
def get_dashboard_stats(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取仪表盘统计数据

    - **current_user**: 当前登录用户（自动注入）
    - **db**: 数据库会话（自动注入）

    返回：
    - **user_count**: 用户总数
    - **role_count**: 角色总数
    - **permission_count**: 权限总数
    - **department_count**: 部门总数
    - **operation_log_count**: 操作日志总数
    - **active_user_count**: 活跃用户数
    """
    tenant_id = current_user.tenant_id
    dashboard_service = DashboardService(db)
    data = dashboard_service.get_dashboard_stats(tenant_id=tenant_id)
    return ResponseUtils.success(data=data, message="获取仪表盘统计数据成功")
