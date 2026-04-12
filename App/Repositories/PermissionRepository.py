"""Permission Repository"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from App.Models.Permission import PermissionModel
from App.Repositories.Base import BaseRepository


class PermissionRepository(BaseRepository[PermissionModel]):
    """权限仓储类"""

    def __init__(self, db: Session):
        """初始化权限仓储"""
        super().__init__(db, PermissionModel)

    def get_by_code(self, code: str, tenant_id: int) -> Optional[PermissionModel]:
        """根据权限编码获取权限"""
        return self.db.query(PermissionModel).filter(
            PermissionModel.code == code,
            PermissionModel.tenant_id == tenant_id,
            PermissionModel.is_deleted == 0
        ).first()

    def get_by_type(self, permission_type: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[PermissionModel]:
        """根据权限类型获取权限"""
        return self.db.query(PermissionModel).filter(
            PermissionModel.type == permission_type,
            PermissionModel.tenant_id == tenant_id,
            PermissionModel.is_deleted == 0,
            PermissionModel.status == 1
        ).offset(skip).limit(limit).all()

    def get_by_resource_type(self, resource_type: str, tenant_id: int, skip: int = 0, limit: int = 100) -> List[PermissionModel]:
        """根据资源类型获取权限"""
        return self.db.query(PermissionModel).filter(
            PermissionModel.resource_type == resource_type,
            PermissionModel.tenant_id == tenant_id,
            PermissionModel.is_deleted == 0,
            PermissionModel.status == 1
        ).offset(skip).limit(limit).all()

    def get_by_parent_id(self, parent_id: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[PermissionModel]:
        """根据父权限ID获取子权限"""
        return self.db.query(PermissionModel).filter(
            PermissionModel.parent_id == parent_id,
            PermissionModel.tenant_id == tenant_id,
            PermissionModel.is_deleted == 0,
            PermissionModel.status == 1
        ).offset(skip).limit(limit).all()

    def get_root_permissions(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[PermissionModel]:
        """获取根权限"""
        return self.db.query(PermissionModel).filter(
            (PermissionModel.parent_id == None) | (PermissionModel.parent_id == 0),
            PermissionModel.tenant_id == tenant_id,
            PermissionModel.is_deleted == 0,
            PermissionModel.status == 1
        ).offset(skip).limit(limit).all()

    def search(self, keyword: str, tenant_id: int, skip: int = 0, limit: int = 100) -> List[PermissionModel]:
        """搜索权限"""
        return self.db.query(PermissionModel).filter(
            or_(
                PermissionModel.name.like(f"%{keyword}%"),
                PermissionModel.code.like(f"%{keyword}%"),
                PermissionModel.path.like(f"%{keyword}%")
            ),
            PermissionModel.tenant_id == tenant_id,
            PermissionModel.is_deleted == 0,
            PermissionModel.status == 1
        ).offset(skip).limit(limit).all()

    def get_active_permissions(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[PermissionModel]:
        """获取活跃权限"""
        return self.db.query(PermissionModel).filter(
            PermissionModel.tenant_id == tenant_id,
            PermissionModel.is_deleted == 0,
            PermissionModel.status == 1
        ).offset(skip).limit(limit).all()

    def get_by_action(self, action: str, tenant_id: int, skip: int = 0, limit: int = 100) -> List[PermissionModel]:
        """根据操作类型获取权限"""
        return self.db.query(PermissionModel).filter(
            PermissionModel.action == action,
            PermissionModel.tenant_id == tenant_id,
            PermissionModel.is_deleted == 0,
            PermissionModel.status == 1
        ).offset(skip).limit(limit).all()

    def paginate(
        self,
        tenant_id: int,
        keyword: str = None,
        permission_type: int = None,
        status: int = None,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[int, List[PermissionModel]]:
        """分页查询权限"""
        query = self.db.query(PermissionModel).filter(
            PermissionModel.tenant_id == tenant_id,
            PermissionModel.is_deleted == 0
        )

        if keyword:
            query = query.filter(
                or_(
                    PermissionModel.name.like(f"%{keyword}%"),
                    PermissionModel.code.like(f"%{keyword}%")
                )
            )

        if permission_type is not None:
            query = query.filter(PermissionModel.type == permission_type)

        if status is not None:
            query = query.filter(PermissionModel.status == status)

        total = query.count()
        items = query.order_by(PermissionModel.create_time.desc()).offset((page - 1) * page_size).limit(page_size).all()

        return total, items
