"""Department Service"""

from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from App.Models.Department import DepartmentModel
from App.Core.Exceptions import ValidationException, NotFoundException
from App.Repositories.DepartmentRepository import DepartmentRepository
from App.Utils.Validators import Validators
from App.Utils.Tree import TreeUtils
from App.Utils.Logger import logger


class DepartmentService:
    """部门服务类"""

    def __init__(self, db: Session):
        """初始化部门服务"""
        self.db = db
        self.department_repository = DepartmentRepository(db)

    def get_department_by_id(self, department_id: int, tenant_id: int) -> DepartmentModel:
        """根据ID获取部门"""
        department = self.department_repository.get_by_id(department_id, tenant_id=tenant_id)
        if not department:
            raise NotFoundException(detail="部门不存在")
        return department

    def get_department_by_code(self, code: str, tenant_id: int) -> DepartmentModel:
        """根据部门编码获取部门"""
        department = self.department_repository.get_by_code(code, tenant_id=tenant_id)
        if not department:
            raise NotFoundException(detail="部门不存在")
        return department

    def get_departments(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[DepartmentModel]:
        """获取部门列表"""
        return self.department_repository.get_all(tenant_id=tenant_id, skip=skip, limit=limit)

    def get_active_departments(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[DepartmentModel]:
        """获取活跃部门列表"""
        return self.department_repository.get_active_departments(tenant_id=tenant_id, skip=skip, limit=limit)

    def get_departments_by_parent_id(self, parent_id: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[DepartmentModel]:
        """根据父部门ID获取子部门列表"""
        if parent_id != 0:
            parent_department = self.department_repository.get_by_id(parent_id, tenant_id=tenant_id)
            if not parent_department:
                raise NotFoundException(detail="父部门不存在")

        return self.department_repository.get_by_parent_id(parent_id, tenant_id=tenant_id, skip=skip, limit=limit)

    def get_root_departments(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[DepartmentModel]:
        """获取根部门列表"""
        return self.department_repository.get_root_departments(tenant_id=tenant_id, skip=skip, limit=limit)

    def search_departments(self, keyword: str, tenant_id: int, skip: int = 0, limit: int = 100) -> List[DepartmentModel]:
        """搜索部门"""
        return self.department_repository.search(keyword, tenant_id=tenant_id, skip=skip, limit=limit)

    def paginate_departments(
        self,
        tenant_id: int,
        keyword: str = None,
        status: int = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[int, List[DepartmentModel]]:
        """分页查询部门"""
        return self.department_repository.paginate(
            tenant_id=tenant_id,
            keyword=keyword,
            status=status,
            page=page,
            page_size=page_size
        )

    def create_department(self, department_data: Dict[str, Any], tenant_id: int, created_by: int) -> DepartmentModel:
        """创建部门"""
        code = department_data.get("code")
        existing_department = self.department_repository.get_by_code(code, tenant_id=tenant_id)
        if existing_department:
            raise ValidationException(detail="部门编码已存在")

        name = department_data.get("name")
        existing_department = self.department_repository.get_by_name(name, tenant_id=tenant_id)
        if existing_department:
            raise ValidationException(detail="部门名称已存在")

        parent_id = department_data.get("parent_id")
        parent_level = 0
        if parent_id and parent_id != 0:
            parent_department = self.department_repository.get_by_id(parent_id, tenant_id=tenant_id)
            if not parent_department:
                raise ValidationException(detail="父部门不存在")
            parent_level = parent_department.level

        department = DepartmentModel(
            name=name,
            code=code,
            parent_id=parent_id,
            level=parent_level + 1,
            leader_id=department_data.get("leader_id"),
            contact_phone=department_data.get("contact_phone"),
            address=department_data.get("address"),
            description=department_data.get("description"),
            status=department_data.get("status", 1),
            tenant_id=tenant_id,
            created_by=created_by,
            updated_by=created_by
        )

        created_department = self.department_repository.create(department)

        logger.info(f"创建部门成功: {name}")

        return created_department

    def update_department(self, department_id: int, department_data: Dict[str, Any], tenant_id: int, updated_by: int) -> DepartmentModel:
        """更新部门"""
        department = self.department_repository.get_by_id(department_id, tenant_id=tenant_id)
        if not department:
            raise NotFoundException(detail="部门不存在")

        code = department_data.get("code")
        if code and code != department.code:
            existing_department = self.department_repository.get_by_code(code, tenant_id=tenant_id)
            if existing_department:
                raise ValidationException(detail="部门编码已存在")
            department.code = code

        name = department_data.get("name")
        if name and name != department.name:
            existing_department = self.department_repository.get_by_name(name, tenant_id=tenant_id)
            if existing_department:
                raise ValidationException(detail="部门名称已存在")
            department.name = name

        parent_id = department_data.get("parent_id")
        if parent_id is not None:
            if parent_id == 0 or parent_id is None:
                department.parent_id = None
                department.level = 1
            else:
                parent_department = self.department_repository.get_by_id(parent_id, tenant_id=tenant_id)
                if not parent_department:
                    raise ValidationException(detail="父部门不存在")
                if parent_id == department_id:
                    raise ValidationException(detail="父部门不能是自身")
                children_ids = self.department_repository.get_department_children_ids(department_id, tenant_id=tenant_id)
                if parent_id in children_ids:
                    raise ValidationException(detail="存在循环依赖")
                department.parent_id = parent_id
                department.level = parent_department.level + 1

        if "leader_id" in department_data:
            department.leader_id = department_data.get("leader_id")

        if "contact_phone" in department_data:
            department.contact_phone = department_data.get("contact_phone")

        if "address" in department_data:
            department.address = department_data.get("address")

        if "description" in department_data:
            department.description = department_data.get("description")

        if "status" in department_data:
            department.status = department_data.get("status")

        department.updated_by = updated_by

        updated_department = self.department_repository.update(department)

        logger.info(f"更新部门成功: {department.name}")

        return updated_department

    def delete_department(self, department_id: int, tenant_id: int) -> bool:
        """删除部门"""
        department = self.department_repository.get_by_id(department_id, tenant_id=tenant_id)
        if not department:
            raise NotFoundException(detail="部门不存在")

        children_departments = self.department_repository.get_by_parent_id(department_id, tenant_id=tenant_id)
        if children_departments:
            raise ValidationException(detail="该部门存在子部门，无法删除")

        from App.Repositories.UserRepository import UserRepository
        user_repository = UserRepository(self.db)
        users = user_repository.get_by_department(department_id, tenant_id=tenant_id)
        user_count = len(users)
        if user_count > 0:
            raise ValidationException(detail=f"该部门已关联 {user_count} 个用户，无法删除")

        self.department_repository.delete(department)

        logger.info(f"删除部门成功: {department.name}")

        return True

    def update_department_status(self, department_id: int, status: int, tenant_id: int, updated_by: int) -> DepartmentModel:
        """更新部门状态"""
        if not Validators.is_status_valid(status):
            raise ValidationException(detail="无效的状态值")

        department = self.department_repository.get_by_id(department_id, tenant_id=tenant_id)
        if not department:
            raise NotFoundException(detail="部门不存在")

        department.status = status
        department.updated_by = updated_by

        updated_department = self.department_repository.update(department)

        logger.info(f"更新部门状态成功: {department.name}, 状态: {status}")

        return updated_department

    def get_department_tree(self, tenant_id: int) -> List[Dict[str, Any]]:
        """获取部门树形结构（管理用，包含所有部门）"""
        from App.Models.Department import DepartmentModel
        departments = self.db.query(DepartmentModel).filter(
            DepartmentModel.tenant_id == tenant_id,
            DepartmentModel.is_deleted == 0
        ).order_by(DepartmentModel.level).all()

        department_list = []
        for dept in departments:
            department_list.append({
                "id": dept.id,
                "name": dept.name,
                "code": dept.code,
                "parent_id": dept.parent_id,
                "level": dept.level,
                "leader_id": dept.leader_id,
                "contact_phone": dept.contact_phone,
                "address": dept.address,
                "description": dept.description,
                "status": dept.status,
                "create_time": dept.create_time.isoformat() if dept.create_time else None,
                "update_time": dept.update_time.isoformat() if dept.update_time else None
            })

        tree = TreeUtils.build_tree(department_list)

        return tree

    def get_department_children(self, department_id: int, tenant_id: int) -> List[DepartmentModel]:
        """获取部门的所有子部门"""
        department = self.department_repository.get_by_id(department_id, tenant_id=tenant_id)
        if not department:
            raise NotFoundException(detail="部门不存在")

        return self.department_repository.get_by_parent_id(department_id, tenant_id=tenant_id)

    def get_department_users(self, department_id: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """获取部门用户列表"""
        department = self.department_repository.get_by_id(department_id, tenant_id=tenant_id)
        if not department:
            raise NotFoundException(detail="部门不存在")

        from App.Repositories.UserRepository import UserRepository
        user_repository = UserRepository(self.db)
        users = user_repository.get_by_department(department_id, tenant_id=tenant_id, skip=skip, limit=limit)

        user_list = []
        for user in users:
            user_list.append({
                "id": user.id,
                "username": user.username,
                "nickname": user.nickname,
                "email": user.email,
                "phone": user.phone,
                "avatar": user.avatar,
                "status": user.status,
                "last_login_time": user.last_login_time
            })

        return user_list

    def count_department_users(self, department_id: int, tenant_id: int) -> int:
        """统计部门用户数量"""
        department = self.department_repository.get_by_id(department_id, tenant_id=tenant_id)
        if not department:
            raise NotFoundException(detail="部门不存在")

        from App.Repositories.UserRepository import UserRepository
        user_repository = UserRepository(self.db)
        users = user_repository.get_by_department(department_id, tenant_id=tenant_id)

        return len(users)
