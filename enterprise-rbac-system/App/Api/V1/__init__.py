"""API V1 Version"""

from fastapi import APIRouter
from App.Api.V1 import (
    Auth, Users, Roles, Permissions, Departments, Menus, Metrics,
    SystemDicts, SystemConfigs, OperationLogs, AuditLogs, UserGroups,
    DataPermissionRules, UserSessions, UserProfiles, Health, Dashboard
)


# 创建V1版本的API路由
api_v1_router = APIRouter(prefix="/v1")

# 注册健康检查路由（放在最前面）
api_v1_router.include_router(Health.router)

# 注册认证路由
api_v1_router.include_router(Auth.router)

# 注册仪表盘路由
api_v1_router.include_router(Dashboard.router)

# 注册用户管理路由
api_v1_router.include_router(Users.router)

# 注册角色管理路由
api_v1_router.include_router(Roles.router)

# 注册权限管理路由
api_v1_router.include_router(Permissions.router)

# 注册部门管理路由
api_v1_router.include_router(Departments.router)

# 注册菜单管理路由
api_v1_router.include_router(Menus.router)

# 注册系统字典管理路由
api_v1_router.include_router(SystemDicts.router)

# 注册系统配置管理路由
api_v1_router.include_router(SystemConfigs.router)

# 注册操作日志管理路由
api_v1_router.include_router(OperationLogs.router)

# 注册审计日志管理路由
api_v1_router.include_router(AuditLogs.router)

# 注册用户组管理路由
api_v1_router.include_router(UserGroups.router)

# 注册数据权限规则管理路由
api_v1_router.include_router(DataPermissionRules.router)

# 注册用户会话管理路由
api_v1_router.include_router(UserSessions.router)

# 注册用户资料管理路由
api_v1_router.include_router(UserProfiles.router)

# 注册监控路由
api_v1_router.include_router(Metrics.router)
