"""Base Repository"""

from typing import List, Optional, TypeVar, Generic, Any
from datetime import datetime
from sqlalchemy.orm import Session, selectinload, joinedload
from sqlalchemy import func, select
from App.Models.Base import BaseModel

# 创建泛型类型
ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """基础仓储类，封装通用的CRUD操作，支持软删除和乐观锁"""
    
    def __init__(self, db: Session, model: type[ModelType]):
        """初始化仓储"""
        self.db = db
        self.model = model
    
    def _apply_tenant_filter(self, query, tenant_id: Optional[int] = None):
        """应用租户过滤"""
        if tenant_id is not None and hasattr(self.model, 'tenant_id'):
            return query.filter(self.model.tenant_id == tenant_id)
        return query
    
    def _apply_soft_delete_filter(self, query, include_deleted: bool = False):
        """应用软删除过滤"""
        if not include_deleted and hasattr(self.model, 'is_deleted'):
            return query.filter(self.model.is_deleted == 0)
        return query
    
    def get_by_id(self, id: int, tenant_id: Optional[int] = None, include_deleted: bool = False) -> Optional[ModelType]:
        """根据ID获取记录"""
        query = self.db.query(self.model).filter(self.model.id == id)
        query = self._apply_tenant_filter(query, tenant_id)
        query = self._apply_soft_delete_filter(query, include_deleted)
        return query.first()
    
    def get_all(self, tenant_id: Optional[int] = None, skip: int = 0, limit: int = 100, include_deleted: bool = False) -> List[ModelType]:
        """获取所有记录"""
        query = self.db.query(self.model)
        query = self._apply_tenant_filter(query, tenant_id)
        query = self._apply_soft_delete_filter(query, include_deleted)
        return query.offset(skip).limit(limit).all()
    
    def get_by_condition(self, condition, tenant_id: Optional[int] = None, skip: int = 0, limit: int = 100, include_deleted: bool = False) -> List[ModelType]:
        """根据条件获取记录"""
        query = self.db.query(self.model).filter(condition)
        query = self._apply_tenant_filter(query, tenant_id)
        query = self._apply_soft_delete_filter(query, include_deleted)
        return query.offset(skip).limit(limit).all()
    
    def create(self, obj: ModelType) -> ModelType:
        """创建记录"""
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def update(self, obj: ModelType, user_id: Optional[int] = None) -> ModelType:
        """更新记录（支持乐观锁）"""
        if hasattr(obj, 'version'):
            obj.version += 1
        if hasattr(obj, 'updated_by') and user_id:
            obj.updated_by = user_id
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def delete(self, obj: ModelType, user_id: Optional[int] = None, soft_delete: bool = True) -> None:
        """删除记录（默认软删除）"""
        if soft_delete and hasattr(obj, 'is_deleted'):
            obj.is_deleted = 1
            if hasattr(obj, 'delete_time'):
                obj.delete_time = datetime.now()
            if hasattr(obj, 'deleted_by') and user_id:
                obj.deleted_by = user_id
            self.db.commit()
        else:
            self.db.delete(obj)
            self.db.commit()
    
    def restore(self, obj: ModelType, user_id: Optional[int] = None) -> Optional[ModelType]:
        """恢复软删除的记录"""
        if hasattr(obj, 'is_deleted'):
            obj.is_deleted = 0
            if hasattr(obj, 'delete_time'):
                obj.delete_time = None
            if hasattr(obj, 'deleted_by'):
                obj.deleted_by = None
            if hasattr(obj, 'updated_by') and user_id:
                obj.updated_by = user_id
            self.db.commit()
            self.db.refresh(obj)
            return obj
        return None
    
    def count(self, condition = None, tenant_id: Optional[int] = None, include_deleted: bool = False) -> int:
        """获取记录数量"""
        query = self.db.query(self.model)
        if condition is not None:
            query = query.filter(condition)
        query = self._apply_tenant_filter(query, tenant_id)
        query = self._apply_soft_delete_filter(query, include_deleted)
        return query.count()
    
    def bulk_create(self, objs: List[ModelType]) -> List[ModelType]:
        """批量创建记录"""
        self.db.add_all(objs)
        self.db.commit()
        return objs
    
    def bulk_update(self, objs: List[ModelType], user_id: Optional[int] = None) -> List[ModelType]:
        """批量更新记录（支持乐观锁）"""
        for obj in objs:
            if hasattr(obj, 'version'):
                obj.version += 1
            if hasattr(obj, 'updated_by') and user_id:
                obj.updated_by = user_id
        self.db.commit()
        return objs
    
    def bulk_delete(self, objs: List[ModelType], user_id: Optional[int] = None, soft_delete: bool = True) -> None:
        """批量删除记录（默认软删除）"""
        if soft_delete:
            for obj in objs:
                if hasattr(obj, 'is_deleted'):
                    obj.is_deleted = 1
                    if hasattr(obj, 'delete_time'):
                        obj.delete_time = datetime.now()
                    if hasattr(obj, 'deleted_by') and user_id:
                        obj.deleted_by = user_id
            self.db.commit()
        else:
            for obj in objs:
                self.db.delete(obj)
            self.db.commit()
    
    def get_by_ids(self, ids: List[int], tenant_id: Optional[int] = None, include_deleted: bool = False) -> List[ModelType]:
        """根据ID列表获取记录"""
        query = self.db.query(self.model).filter(self.model.id.in_(ids))
        query = self._apply_tenant_filter(query, tenant_id)
        query = self._apply_soft_delete_filter(query, include_deleted)
        return query.all()
    
    def exists(self, condition, tenant_id: Optional[int] = None, include_deleted: bool = False) -> bool:
        """检查记录是否存在"""
        query = self.db.query(self.model).filter(condition)
        query = self._apply_tenant_filter(query, tenant_id)
        query = self._apply_soft_delete_filter(query, include_deleted)
        return query.first() is not None
    
    def count_optimized(self, condition = None, tenant_id: Optional[int] = None, include_deleted: bool = False) -> int:
        """优化的count查询，使用COUNT(1)"""
        query = self.db.query(func.count(1))
        if condition is not None:
            query = query.filter(condition)
        query = self._apply_tenant_filter(query, tenant_id)
        query = self._apply_soft_delete_filter(query, include_deleted)
        return query.scalar() or 0
    
    def exists_optimized(self, condition, tenant_id: Optional[int] = None, include_deleted: bool = False) -> bool:
        """优化的exists查询，使用LIMIT 1"""
        query = self.db.query(func.count(1)).filter(condition)
        query = self._apply_tenant_filter(query, tenant_id)
        query = self._apply_soft_delete_filter(query, include_deleted)
        query = query.limit(1)
        return query.scalar() > 0
    
    def get_with_related(self, id: int, related: List[str], tenant_id: Optional[int] = None, include_deleted: bool = False) -> Optional[ModelType]:
        """获取记录并预加载关联数据"""
        query = self.db.query(self.model)
        
        for relation in related:
            if '__' in relation:
                parts = relation.split('__')
                current_load = None
                for i, part in enumerate(parts):
                    if i == 0:
                        current_load = selectinload(getattr(self.model, part))
                    else:
                        current_load = current_load.selectinload(getattr(parts[i-1], part))
                query = query.options(current_load)
            else:
                query = query.options(selectinload(getattr(self.model, relation)))
        
        query = query.filter(self.model.id == id)
        query = self._apply_tenant_filter(query, tenant_id)
        query = self._apply_soft_delete_filter(query, include_deleted)
        return query.first()
    
    def paginate_optimized(
        self,
        tenant_id: Optional[int] = None,
        keyword: str = None,
        condition = None,
        include_deleted: bool = False,
        page: int = 1,
        page_size: int = 20,
        order_by: Any = None,
        related: List[str] = None
    ) -> tuple[int, List[ModelType]]:
        """优化的分页查询"""
        query = self.db.query(self.model)
        
        if related:
            for relation in related:
                query = query.options(selectinload(getattr(self.model, relation)))
        
        query = self._apply_tenant_filter(query, tenant_id)
        query = self._apply_soft_delete_filter(query, include_deleted)
        
        if condition is not None:
            query = query.filter(condition)
        
        total = self.count_optimized(condition=condition, tenant_id=tenant_id, include_deleted=include_deleted)
        
        if order_by is None and hasattr(self.model, 'create_time'):
            order_by = self.model.create_time.desc()
        
        if order_by is not None:
            query = query.order_by(order_by)
        
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        return total, items