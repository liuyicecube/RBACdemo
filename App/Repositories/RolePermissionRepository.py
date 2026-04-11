"""Role Permission Repository"""

from typing import List, Optional
from sqlalchemy.orm import Session
from App.Models.RolePermission import RolePermissionModel
from App.Repositories.Base import BaseRepository


class RolePermissionRepository(BaseRepository[RolePermissionModel]):
    """角色权限关联仓储类"""
    
    def __init__(self, db: Session):
        """初始化角色权限关联仓储"""
        super().__init__(db, RolePermissionModel)
    
    def get_by_role_id(self, role_id: int, tenant_id: int) -> List[RolePermissionModel]:
        """根据角色ID获取权限关联"""
        return self.db.query(RolePermissionModel).filter(
            RolePermissionModel.role_id == role_id,
            RolePermissionModel.tenant_id == tenant_id,
            RolePermissionModel.is_deleted == 0,
            RolePermissionModel.status == 1
        ).all()
    
    def get_by_permission_id(self, permission_id: int, tenant_id: int) -> List[RolePermissionModel]:
        """根据权限ID获取角色关联"""
        return self.db.query(RolePermissionModel).filter(
            RolePermissionModel.permission_id == permission_id,
            RolePermissionModel.tenant_id == tenant_id,
            RolePermissionModel.is_deleted == 0,
            RolePermissionModel.status == 1
        ).all()
    
    def get_by_role_and_permission(self, role_id: int, permission_id: int, tenant_id: int) -> Optional[RolePermissionModel]:
        """根据角色ID和权限ID获取关联"""
        return self.db.query(RolePermissionModel).filter(
            RolePermissionModel.role_id == role_id,
            RolePermissionModel.permission_id == permission_id,
            RolePermissionModel.tenant_id == tenant_id,
            RolePermissionModel.is_deleted == 0
        ).first()
    
    def delete_by_role_id(self, role_id: int, tenant_id: int) -> None:
        """根据角色ID删除所有权限关联"""
        self.db.query(RolePermissionModel).filter(
            RolePermissionModel.role_id == role_id,
            RolePermissionModel.tenant_id == tenant_id
        ).delete()
        self.db.commit()
    
    def delete_by_permission_id(self, permission_id: int, tenant_id: int) -> None:
        """根据权限ID删除所有角色关联"""
        self.db.query(RolePermissionModel).filter(
            RolePermissionModel.permission_id == permission_id,
            RolePermissionModel.tenant_id == tenant_id
        ).delete()
        self.db.commit()
    
    def count_by_role_id(self, role_id: int, tenant_id: int) -> int:
        """统计角色关联的权限数量"""
        return self.db.query(RolePermissionModel).filter(
            RolePermissionModel.role_id == role_id,
            RolePermissionModel.tenant_id == tenant_id,
            RolePermissionModel.is_deleted == 0,
            RolePermissionModel.status == 1
        ).count()
    
    def count_by_permission_id(self, permission_id: int, tenant_id: int) -> int:
        """统计权限关联的角色数量"""
        return self.db.query(RolePermissionModel).filter(
            RolePermissionModel.permission_id == permission_id,
            RolePermissionModel.tenant_id == tenant_id,
            RolePermissionModel.is_deleted == 0,
            RolePermissionModel.status == 1
        ).count()
    
    def bulk_create(self, role_id: int, permission_ids: List[int], tenant_id: int, operator_id: int = None) -> List[RolePermissionModel]:
        """批量创建角色权限关联"""
        # 先删除现有关联
        self.delete_by_role_id(role_id, tenant_id)
        
        # 创建新关联
        role_permissions = []
        for permission_id in permission_ids:
            role_permission = RolePermissionModel(
                role_id=role_id,
                permission_id=permission_id,
                tenant_id=tenant_id,
                created_by=operator_id
            )
            role_permissions.append(role_permission)
        
        if role_permissions:
            self.db.add_all(role_permissions)
            self.db.commit()
        
        return role_permissions