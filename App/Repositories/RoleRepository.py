"""Role Repository"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from App.Models.Role import RoleModel
from App.Repositories.Base import BaseRepository


class RoleRepository(BaseRepository[RoleModel]):
    """角色仓储类"""

    def __init__(self, db: Session):
        """初始化角色仓储"""
        super().__init__(db, RoleModel)

    def get_by_code(self, code: str, tenant_id: int) -> Optional[RoleModel]:
        """根据角色编码获取角色"""
        return self.db.query(RoleModel).filter(
            RoleModel.code == code,
            RoleModel.tenant_id == tenant_id,
            RoleModel.is_deleted == 0
        ).first()

    def get_by_name(self, name: str, tenant_id: int) -> Optional[RoleModel]:
        """根据角色名称获取角色"""
        return self.db.query(RoleModel).filter(
            RoleModel.name == name,
            RoleModel.tenant_id == tenant_id,
            RoleModel.is_deleted == 0
        ).first()

    def get_by_type(self, role_type: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[RoleModel]:
        """根据角色类型获取角色"""
        return self.db.query(RoleModel).filter(
            RoleModel.type == role_type,
            RoleModel.tenant_id == tenant_id,
            RoleModel.is_deleted == 0,
            RoleModel.status == 1
        ).offset(skip).limit(limit).all()

    def get_by_parent_id(self, parent_id: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[RoleModel]:
        """根据父角色ID获取子角色"""
        return self.db.query(RoleModel).filter(
            RoleModel.parent_id == parent_id,
            RoleModel.tenant_id == tenant_id,
            RoleModel.is_deleted == 0,
            RoleModel.status == 1
        ).offset(skip).limit(limit).all()

    def get_root_roles(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[RoleModel]:
        """获取根角色"""
        return self.db.query(RoleModel).filter(
            (RoleModel.parent_id == None) | (RoleModel.parent_id == 0),
            RoleModel.tenant_id == tenant_id,
            RoleModel.is_deleted == 0,
            RoleModel.status == 1
        ).offset(skip).limit(limit).all()

    def search(self, keyword: str, tenant_id: int, skip: int = 0, limit: int = 100) -> List[RoleModel]:
        """搜索角色"""
        return self.db.query(RoleModel).filter(
            or_(
                RoleModel.name.like(f"%{keyword}%"),
                RoleModel.code.like(f"%{keyword}%"),
                RoleModel.description.like(f"%{keyword}%")
            ),
            RoleModel.tenant_id == tenant_id,
            RoleModel.is_deleted == 0,
            RoleModel.status == 1
        ).offset(skip).limit(limit).all()

    def get_active_roles(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[RoleModel]:
        """获取活跃角色"""
        return self.db.query(RoleModel).filter(
            RoleModel.tenant_id == tenant_id,
            RoleModel.is_deleted == 0,
            RoleModel.status == 1
        ).offset(skip).limit(limit).all()

    def get_inactive_roles(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[RoleModel]:
        """获取非活跃角色"""
        return self.db.query(RoleModel).filter(
            RoleModel.tenant_id == tenant_id,
            RoleModel.is_deleted == 0,
            RoleModel.status == 0
        ).offset(skip).limit(limit).all()

    def get_role_children_ids(self, role_id: int, tenant_id: int) -> List[int]:
        """获取角色的所有子角色ID"""
        # 递归获取所有子角色ID
        def _get_children_ids(rid: int) -> List[int]:
            children = self.db.query(RoleModel.id).filter(
                RoleModel.parent_id == rid,
                RoleModel.tenant_id == tenant_id,
                RoleModel.is_deleted == 0
            ).all()
            children_ids = [child.id for child in children]
            for child_id in children_ids:
                children_ids.extend(_get_children_ids(child_id))
            return children_ids

        return _get_children_ids(role_id)

    def paginate(
        self,
        tenant_id: int,
        keyword: str = None,
        role_type: int = None,
        status: int = None,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[int, List[RoleModel]]:
        """分页查询角色"""
        query = self.db.query(RoleModel).filter(
            RoleModel.tenant_id == tenant_id,
            RoleModel.is_deleted == 0
        )

        if keyword:
            query = query.filter(
                or_(
                    RoleModel.name.like(f"%{keyword}%"),
                    RoleModel.code.like(f"%{keyword}%")
                )
            )

        if role_type is not None:
            query = query.filter(RoleModel.type == role_type)

        if status is not None:
            query = query.filter(RoleModel.status == status)

        total = query.count()
        items = query.order_by(RoleModel.sort, RoleModel.create_time.desc()).offset((page - 1) * page_size).limit(page_size).all()

        return total, items
