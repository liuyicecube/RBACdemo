"""Operation Log Repository"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from datetime import datetime, timedelta
from App.Models.OperationLog import OperationLogModel
from App.Repositories.Base import BaseRepository


class OperationLogRepository(BaseRepository[OperationLogModel]):
    """操作日志仓储类"""
    
    def __init__(self, db: Session):
        """初始化操作日志仓储"""
        super().__init__(db, OperationLogModel)
    
    def get_by_user_id(self, user_id: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[OperationLogModel]:
        """根据用户ID获取日志"""
        return self.db.query(OperationLogModel).filter(
            OperationLogModel.user_id == user_id,
            OperationLogModel.tenant_id == tenant_id
        ).order_by(OperationLogModel.create_time.desc()).offset(skip).limit(limit).all()
    
    def get_by_module(self, module: str, tenant_id: int, skip: int = 0, limit: int = 100) -> List[OperationLogModel]:
        """根据模块获取日志"""
        return self.db.query(OperationLogModel).filter(
            OperationLogModel.module == module,
            OperationLogModel.tenant_id == tenant_id
        ).order_by(OperationLogModel.create_time.desc()).offset(skip).limit(limit).all()
    
    def get_by_date_range(self, start_time: datetime, end_time: datetime, tenant_id: int, skip: int = 0, limit: int = 100) -> List[OperationLogModel]:
        """根据时间范围获取日志"""
        return self.db.query(OperationLogModel).filter(
            OperationLogModel.create_time >= start_time,
            OperationLogModel.create_time <= end_time,
            OperationLogModel.tenant_id == tenant_id
        ).order_by(OperationLogModel.create_time.desc()).offset(skip).limit(limit).all()
    
    def get_failed_logs(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[OperationLogModel]:
        """获取失败的日志"""
        return self.db.query(OperationLogModel).filter(
            OperationLogModel.status == 0,
            OperationLogModel.tenant_id == tenant_id
        ).order_by(OperationLogModel.create_time.desc()).offset(skip).limit(limit).all()
    
    def delete_old_logs(self, days: int, tenant_id: int):
        """删除指定天数之前的日志"""
        cutoff_time = datetime.now() - timedelta(days=days)
        self.db.query(OperationLogModel).filter(
            OperationLogModel.create_time < cutoff_time,
            OperationLogModel.tenant_id == tenant_id
        ).delete(synchronize_session=False)
    
    def paginate(
        self,
        tenant_id: int,
        keyword: str = None,
        module: str = None,
        user_id: int = None,
        status: int = None,
        start_time: datetime = None,
        end_time: datetime = None,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[int, List[OperationLogModel]]:
        """分页查询操作日志"""
        query = self.db.query(OperationLogModel).filter(
            OperationLogModel.tenant_id == tenant_id
        )
        
        if keyword:
            query = query.filter(
                or_(
                    OperationLogModel.username.like(f"%{keyword}%"),
                    OperationLogModel.module.like(f"%{keyword}%"),
                    OperationLogModel.operation.like(f"%{keyword}%"),
                    OperationLogModel.url.like(f"%{keyword}%"),
                    OperationLogModel.ip.like(f"%{keyword}%")
                )
            )
        
        if module:
            query = query.filter(OperationLogModel.module == module)
        
        if user_id:
            query = query.filter(OperationLogModel.user_id == user_id)
        
        if status is not None:
            query = query.filter(OperationLogModel.status == status)
        
        if start_time:
            query = query.filter(OperationLogModel.create_time >= start_time)
        
        if end_time:
            query = query.filter(OperationLogModel.create_time <= end_time)
        
        total = query.count()
        items = query.order_by(OperationLogModel.create_time.desc()).offset((page - 1) * page_size).limit(page_size).all()
        
        return total, items
