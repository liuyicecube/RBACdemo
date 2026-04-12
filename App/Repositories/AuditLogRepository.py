"""Audit Log Repository"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timedelta
from App.Models.AuditLog import AuditLogModel
from App.Repositories.Base import BaseRepository


class AuditLogRepository(BaseRepository[AuditLogModel]):
    """审计日志仓储类"""

    def __init__(self, db: Session):
        """初始化审计日志仓储"""
        super().__init__(db, AuditLogModel)

    def get_by_table_name(self, table_name: str, tenant_id: int, skip: int = 0, limit: int = 100) -> List[AuditLogModel]:
        """根据表名获取日志"""
        return self.db.query(AuditLogModel).filter(
            AuditLogModel.table_name == table_name,
            AuditLogModel.tenant_id == tenant_id
        ).order_by(AuditLogModel.create_time.desc()).offset(skip).limit(limit).all()

    def get_by_record_id(self, table_name: str, record_id: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[AuditLogModel]:
        """根据记录ID获取日志"""
        return self.db.query(AuditLogModel).filter(
            AuditLogModel.table_name == table_name,
            AuditLogModel.record_id == record_id,
            AuditLogModel.tenant_id == tenant_id
        ).order_by(AuditLogModel.create_time.desc()).offset(skip).limit(limit).all()

    def get_by_user_id(self, user_id: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[AuditLogModel]:
        """根据用户ID获取日志"""
        return self.db.query(AuditLogModel).filter(
            AuditLogModel.user_id == user_id,
            AuditLogModel.tenant_id == tenant_id
        ).order_by(AuditLogModel.create_time.desc()).offset(skip).limit(limit).all()

    def delete_old_logs(self, days: int, tenant_id: int):
        """删除指定天数之前的日志"""
        cutoff_time = datetime.now() - timedelta(days=days)
        self.db.query(AuditLogModel).filter(
            AuditLogModel.create_time < cutoff_time,
            AuditLogModel.tenant_id == tenant_id
        ).delete(synchronize_session=False)

    def paginate(
        self,
        tenant_id: int,
        keyword: str = None,
        table_name: str = None,
        record_id: int = None,
        operation_type: str = None,
        user_id: int = None,
        start_time: datetime = None,
        end_time: datetime = None,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[int, List[AuditLogModel]]:
        """分页查询审计日志"""
        query = self.db.query(AuditLogModel).filter(
            AuditLogModel.tenant_id == tenant_id
        )

        if keyword:
            query = query.filter(
                or_(
                    AuditLogModel.username.like(f"%{keyword}%"),
                    AuditLogModel.table_name.like(f"%{keyword}%"),
                    AuditLogModel.change_fields.like(f"%{keyword}%")
                )
            )

        if table_name:
            query = query.filter(AuditLogModel.table_name == table_name)

        if record_id:
            query = query.filter(AuditLogModel.record_id == record_id)

        if operation_type:
            query = query.filter(AuditLogModel.operation_type == operation_type)

        if user_id:
            query = query.filter(AuditLogModel.user_id == user_id)

        if start_time:
            query = query.filter(AuditLogModel.create_time >= start_time)

        if end_time:
            query = query.filter(AuditLogModel.create_time <= end_time)

        total = query.count()
        items = query.order_by(AuditLogModel.create_time.desc()).offset((page - 1) * page_size).limit(page_size).all()

        return total, items
