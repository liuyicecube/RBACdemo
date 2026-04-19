"""Dashboard Service"""

from typing import Dict, Any
from sqlalchemy.orm import Session
from App.Repositories.UserRepository import UserRepository
from App.Repositories.RoleRepository import RoleRepository
from App.Repositories.PermissionRepository import PermissionRepository
from App.Repositories.DepartmentRepository import DepartmentRepository
from App.Repositories.OperationLogRepository import OperationLogRepository
from App.Utils.Logger import logger


class DashboardService:
    """仪表盘服务类"""

    def __init__(self, db: Session):
        """初始化仪表盘服务"""
        self.db = db
        self.user_repository = UserRepository(db)
        self.role_repository = RoleRepository(db)
        self.permission_repository = PermissionRepository(db)
        self.department_repository = DepartmentRepository(db)
        self.operation_log_repository = OperationLogRepository(db)

    def get_dashboard_stats(self, tenant_id: int = None) -> Dict[str, Any]:
        """
        获取仪表盘统计数据

        返回：
        - user_count: 用户总数
        - role_count: 角色总数
        - permission_count: 权限总数
        - department_count: 部门总数
        - operation_log_count: 操作日志总数
        - active_user_count: 活跃用户数
        """
        try:
            logger.info(f"开始获取仪表盘统计数据, tenant_id={tenant_id}")
            
            # 获取各项统计数据
            user_count = self.user_repository.count_optimized(tenant_id=tenant_id)
            logger.info(f"用户总数: {user_count}")
            
            role_count = self.role_repository.count_optimized(tenant_id=tenant_id)
            logger.info(f"角色总数: {role_count}")
            
            permission_count = self.permission_repository.count_optimized(tenant_id=tenant_id)
            logger.info(f"权限总数: {permission_count}")
            
            department_count = self.department_repository.count_optimized(tenant_id=tenant_id)
            logger.info(f"部门总数: {department_count}")
            
            operation_log_count = self.operation_log_repository.count_optimized(tenant_id=tenant_id)
            logger.info(f"操作日志总数: {operation_log_count}")
            
            # 获取活跃用户数（status=1）
            from App.Models.User import UserModel
            active_user_count = self.user_repository.count_optimized(
                condition=UserModel.status == 1,
                tenant_id=tenant_id
            )
            logger.info(f"活跃用户数: {active_user_count}")

            stats = {
                "user_count": user_count,
                "role_count": role_count,
                "permission_count": permission_count,
                "department_count": department_count,
                "operation_log_count": operation_log_count,
                "active_user_count": active_user_count
            }

            logger.info(f"获取仪表盘统计数据成功: {stats}")
            return stats

        except Exception as e:
            logger.error(f"获取仪表盘统计数据失败: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            raise
