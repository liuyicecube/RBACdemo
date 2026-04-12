"""Data Permission Rule Repository"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from App.Models.DataPermissionRule import DataPermissionRuleModel
from App.Repositories.Base import BaseRepository


class DataPermissionRuleRepository(BaseRepository[DataPermissionRuleModel]):
    """数据权限规则仓储类"""

    def __init__(self, db: Session):
        """初始化数据权限规则仓储"""
        super().__init__(db, DataPermissionRuleModel)

    def get_by_code(self, code: str, tenant_id: int) -> Optional[DataPermissionRuleModel]:
        """根据编码获取数据权限规则"""
        return self.db.query(DataPermissionRuleModel).filter(
            DataPermissionRuleModel.code == code,
            DataPermissionRuleModel.tenant_id == tenant_id,
            DataPermissionRuleModel.is_deleted == 0
        ).first()

    def get_by_permission_id(self, permission_id: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[DataPermissionRuleModel]:
        """根据权限ID获取数据权限规则"""
        return self.db.query(DataPermissionRuleModel).filter(
            DataPermissionRuleModel.permission_id == permission_id,
            DataPermissionRuleModel.tenant_id == tenant_id,
            DataPermissionRuleModel.is_deleted == 0
        ).offset(skip).limit(limit).all()

    def get_by_rule_type(self, rule_type: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[DataPermissionRuleModel]:
        """根据规则类型获取数据权限规则"""
        return self.db.query(DataPermissionRuleModel).filter(
            DataPermissionRuleModel.rule_type == rule_type,
            DataPermissionRuleModel.tenant_id == tenant_id,
            DataPermissionRuleModel.is_deleted == 0,
            DataPermissionRuleModel.status == 1
        ).offset(skip).limit(limit).all()

    def get_by_resource_table(self, resource_table: str, tenant_id: int, skip: int = 0, limit: int = 100) -> List[DataPermissionRuleModel]:
        """根据资源表名获取数据权限规则"""
        return self.db.query(DataPermissionRuleModel).filter(
            DataPermissionRuleModel.resource_table == resource_table,
            DataPermissionRuleModel.tenant_id == tenant_id,
            DataPermissionRuleModel.is_deleted == 0,
            DataPermissionRuleModel.status == 1
        ).offset(skip).limit(limit).all()

    def get_active_rules(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[DataPermissionRuleModel]:
        """获取活跃的数据权限规则"""
        return self.db.query(DataPermissionRuleModel).filter(
            DataPermissionRuleModel.tenant_id == tenant_id,
            DataPermissionRuleModel.is_deleted == 0,
            DataPermissionRuleModel.status == 1
        ).offset(skip).limit(limit).all()

    def search(self, keyword: str, tenant_id: int, skip: int = 0, limit: int = 100) -> List[DataPermissionRuleModel]:
        """搜索数据权限规则"""
        return self.db.query(DataPermissionRuleModel).filter(
            or_(
                DataPermissionRuleModel.name.like(f"%{keyword}%"),
                DataPermissionRuleModel.code.like(f"%{keyword}%"),
                DataPermissionRuleModel.resource_table.like(f"%{keyword}%")
            ),
            DataPermissionRuleModel.tenant_id == tenant_id,
            DataPermissionRuleModel.is_deleted == 0
        ).offset(skip).limit(limit).all()

    def paginate(
        self,
        tenant_id: int,
        keyword: str = None,
        permission_id: int = None,
        rule_type: int = None,
        status: int = None,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[int, List[DataPermissionRuleModel]]:
        """分页查询数据权限规则"""
        query = self.db.query(DataPermissionRuleModel).filter(
            DataPermissionRuleModel.tenant_id == tenant_id,
            DataPermissionRuleModel.is_deleted == 0
        )

        if keyword:
            query = query.filter(
                or_(
                    DataPermissionRuleModel.name.like(f"%{keyword}%"),
                    DataPermissionRuleModel.code.like(f"%{keyword}%"),
                    DataPermissionRuleModel.resource_table.like(f"%{keyword}%")
                )
            )

        if permission_id is not None:
            query = query.filter(DataPermissionRuleModel.permission_id == permission_id)

        if rule_type is not None:
            query = query.filter(DataPermissionRuleModel.rule_type == rule_type)

        if status is not None:
            query = query.filter(DataPermissionRuleModel.status == status)

        total = query.count()
        items = query.order_by(DataPermissionRuleModel.create_time.desc()).offset((page - 1) * page_size).limit(page_size).all()

        return total, items
