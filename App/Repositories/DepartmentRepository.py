"""Department Repository"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from App.Models.Department import DepartmentModel
from App.Repositories.Base import BaseRepository


class DepartmentRepository(BaseRepository[DepartmentModel]):
    """部门仓储类"""
    
    def __init__(self, db: Session):
        """初始化部门仓储"""
        super().__init__(db, DepartmentModel)
    
    def get_by_code(self, code: str, tenant_id: int) -> Optional[DepartmentModel]:
        """根据部门编码获取部门"""
        return self.db.query(DepartmentModel).filter(
            DepartmentModel.code == code,
            DepartmentModel.tenant_id == tenant_id,
            DepartmentModel.is_deleted == 0
        ).first()
    
    def get_by_name(self, name: str, tenant_id: int) -> Optional[DepartmentModel]:
        """根据部门名称获取部门"""
        return self.db.query(DepartmentModel).filter(
            DepartmentModel.name == name,
            DepartmentModel.tenant_id == tenant_id,
            DepartmentModel.is_deleted == 0
        ).first()
    
    def get_by_parent_id(self, parent_id: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[DepartmentModel]:
        """根据父部门ID获取子部门"""
        return self.db.query(DepartmentModel).filter(
            DepartmentModel.parent_id == parent_id,
            DepartmentModel.tenant_id == tenant_id,
            DepartmentModel.is_deleted == 0,
            DepartmentModel.status == 1
        ).offset(skip).limit(limit).all()
    
    def get_root_departments(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[DepartmentModel]:
        """获取根部门"""
        return self.db.query(DepartmentModel).filter(
            (DepartmentModel.parent_id == None) | (DepartmentModel.parent_id == 0),
            DepartmentModel.tenant_id == tenant_id,
            DepartmentModel.is_deleted == 0,
            DepartmentModel.status == 1
        ).offset(skip).limit(limit).all()
    
    def search(self, keyword: str, tenant_id: int, skip: int = 0, limit: int = 100) -> List[DepartmentModel]:
        """搜索部门"""
        return self.db.query(DepartmentModel).filter(
            or_(
                DepartmentModel.name.like(f"%{keyword}%"),
                DepartmentModel.code.like(f"%{keyword}%"),
                DepartmentModel.description.like(f"%{keyword}%")
            ),
            DepartmentModel.tenant_id == tenant_id,
            DepartmentModel.is_deleted == 0,
            DepartmentModel.status == 1
        ).offset(skip).limit(limit).all()
    
    def get_active_departments(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[DepartmentModel]:
        """获取活跃部门"""
        return self.db.query(DepartmentModel).filter(
            DepartmentModel.tenant_id == tenant_id,
            DepartmentModel.is_deleted == 0,
            DepartmentModel.status == 1
        ).offset(skip).limit(limit).all()
    
    def get_department_children_ids(self, department_id: int, tenant_id: int) -> List[int]:
        """获取部门的所有子部门ID"""
        # 递归获取所有子部门ID
        def _get_children_ids(dep_id: int) -> List[int]:
            children = self.db.query(DepartmentModel.id).filter(
                DepartmentModel.parent_id == dep_id,
                DepartmentModel.tenant_id == tenant_id,
                DepartmentModel.is_deleted == 0
            ).all()
            children_ids = [child.id for child in children]
            for child_id in children_ids:
                children_ids.extend(_get_children_ids(child_id))
            return children_ids
        
        return _get_children_ids(department_id)
    
    def paginate(
        self,
        tenant_id: int,
        keyword: str = None,
        status: int = None,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[int, List[DepartmentModel]]:
        """分页查询部门"""
        query = self.db.query(DepartmentModel).filter(
            DepartmentModel.tenant_id == tenant_id,
            DepartmentModel.is_deleted == 0
        )
        
        if keyword:
            query = query.filter(
                or_(
                    DepartmentModel.name.like(f"%{keyword}%"),
                    DepartmentModel.code.like(f"%{keyword}%")
                )
            )
        
        if status is not None:
            query = query.filter(DepartmentModel.status == status)
        
        total = query.count()
        items = query.order_by(DepartmentModel.create_time.desc()).offset((page - 1) * page_size).limit(page_size).all()
        
        return total, items