"""User Service"""

from typing import List, Dict, Any, Tuple, Optional
from sqlalchemy.orm import Session
from App.Models.User import UserModel
from App.Core.Exceptions import ValidationException, NotFoundException
from App.Repositories.UserRepository import UserRepository
from App.Repositories.DepartmentRepository import DepartmentRepository
from App.Repositories.UserRoleRepository import UserRoleRepository
from App.Utils.Validators import Validators
from App.Utils.Logger import logger
from App.Core.Security import SecurityCore


class UserService:
    """用户服务类"""

    def __init__(self, db: Session):
        """初始化用户服务"""
        self.db = db
        self.user_repository = UserRepository(db)
        self.department_repository = DepartmentRepository(db)
        self.user_role_repository = UserRoleRepository(db)

    def get_user_by_id(self, user_id: int, tenant_id: Optional[int] = None) -> UserModel:
        """根据ID获取用户（支持tenant_id为None用于获取当前用户）"""
        user = self.user_repository.get_by_id(user_id, tenant_id=tenant_id)
        if not user:
            raise NotFoundException(detail="用户不存在")
        return user

    def get_user_by_username(self, username: str, tenant_id: int) -> UserModel:
        """根据用户名获取用户"""
        user = self.user_repository.get_by_username(username, tenant_id=tenant_id)
        if not user:
            raise NotFoundException(detail="用户不存在")
        return user

    def get_users(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserModel]:
        """获取用户列表"""
        return self.user_repository.get_all(tenant_id=tenant_id, skip=skip, limit=limit)

    def get_active_users(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserModel]:
        """获取活跃用户列表"""
        return self.user_repository.get_active_users(tenant_id=tenant_id, skip=skip, limit=limit)

    def get_inactive_users(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserModel]:
        """获取非活跃用户列表"""
        return self.user_repository.get_inactive_users(tenant_id=tenant_id, skip=skip, limit=limit)

    def get_users_by_department(self, department_id: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserModel]:
        """根据部门ID获取用户列表"""
        department = self.department_repository.get_by_id(department_id, tenant_id=tenant_id)
        if not department:
            raise NotFoundException(detail="部门不存在")

        return self.user_repository.get_by_department(department_id, tenant_id=tenant_id, skip=skip, limit=limit)

    def search_users(self, keyword: str, tenant_id: int, skip: int = 0, limit: int = 100) -> List[UserModel]:
        """搜索用户"""
        return self.user_repository.search(keyword, tenant_id=tenant_id, skip=skip, limit=limit)

    def paginate_users(
        self,
        tenant_id: int,
        keyword: str = None,
        department_id: int = None,
        status: int = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[int, List[UserModel]]:
        """分页查询用户"""
        return self.user_repository.paginate(
            tenant_id=tenant_id,
            keyword=keyword,
            department_id=department_id,
            status=status,
            page=page,
            page_size=page_size
        )

    def create_user(self, user_data: Dict[str, Any], tenant_id: int, created_by: int) -> UserModel:
        """创建用户"""
        if not Validators.is_username_valid(user_data.get("username")):
            raise ValidationException(detail="用户名格式不正确")

        email = user_data.get("email")
        if email and not Validators.is_email(email):
            raise ValidationException(detail="邮箱格式不正确")

        phone = user_data.get("phone")
        if phone and not Validators.is_phone(phone):
            raise ValidationException(detail="手机号格式不正确")

        existing_user = self.user_repository.get_by_username(user_data.get("username"), tenant_id=tenant_id)
        if existing_user:
            raise ValidationException(detail="用户名已存在")

        if email and self.user_repository.get_by_email(email, tenant_id=tenant_id):
            raise ValidationException(detail="邮箱已存在")

        if phone and self.user_repository.get_by_phone(phone, tenant_id=tenant_id):
            raise ValidationException(detail="手机号已存在")

        department_id = user_data.get("department_id")
        if department_id:
            department = self.department_repository.get_by_id(department_id, tenant_id=tenant_id)
            if not department:
                raise ValidationException(detail="部门不存在")

        hashed_password = SecurityCore.get_password_hash(user_data.get("password"))

        user = UserModel(
            username=user_data.get("username"),
            password=hashed_password,
            nickname=user_data.get("nickname"),
            email=email,
            phone=phone,
            department_id=department_id,
            status=user_data.get("status", 1),
            tenant_id=tenant_id,
            created_by=created_by,
            updated_by=created_by
        )

        created_user = self.user_repository.create(user)

        logger.info(f"创建用户成功: {user_data.get('username')}")

        return created_user

    def update_user(self, user_id: int, user_data: Dict[str, Any], tenant_id: int, updated_by: int) -> UserModel:
        """更新用户"""
        logger.info(f"[START] update_user - 用户ID: {user_id}")

        user = self.user_repository.get_by_id(user_id, tenant_id=tenant_id)
        if not user:
            raise NotFoundException(detail="用户不存在")

        if "password" in user_data and user_data.get("password"):
            hashed_password = SecurityCore.get_password_hash(user_data.get("password"))
            user.password = hashed_password

        username = user_data.get("username")
        if username and username != user.username:
            existing_user = self.user_repository.get_by_username(username, tenant_id=tenant_id)
            if existing_user:
                raise ValidationException(detail="用户名已存在")
            user.username = username

        email = user_data.get("email")
        if email and email != user.email:
            existing_user = self.user_repository.get_by_email(email, tenant_id=tenant_id)
            if existing_user:
                raise ValidationException(detail="邮箱已存在")
            user.email = email

        phone = user_data.get("phone")
        if phone and phone != user.phone:
            existing_user = self.user_repository.get_by_phone(phone, tenant_id=tenant_id)
            if existing_user:
                raise ValidationException(detail="手机号已存在")
            user.phone = phone

        department_id = user_data.get("department_id")
        if department_id is not None:
            if department_id == 0 or department_id is None:
                user.department_id = None
            else:
                department = self.department_repository.get_by_id(department_id, tenant_id=tenant_id)
                if not department:
                    raise ValidationException(detail="部门不存在")
                user.department_id = department_id

        if "nickname" in user_data:
            user.nickname = user_data.get("nickname")

        if "avatar" in user_data:
            user.avatar = user_data.get("avatar")

        if "status" in user_data:
            user.status = user_data.get("status")

        user.updated_by = updated_by

        updated_user = self.user_repository.update(user)

        logger.info(f"更新用户成功: {user.username}")

        return updated_user

    def delete_user(self, user_id: int, tenant_id: int, deleted_by: int = None) -> bool:
        """删除用户"""
        user = self.user_repository.get_by_id(user_id, tenant_id=tenant_id)
        if not user:
            raise NotFoundException(detail="用户不存在")

        self.user_role_repository.delete_by_user_id(user_id, tenant_id=tenant_id)

        self.user_repository.delete(user, user_id=deleted_by)

        logger.info(f"删除用户成功: {user.username}")

        return True

    def update_user_status(self, user_id: int, status: int, tenant_id: int, updated_by: int) -> UserModel:
        """更新用户状态"""
        if not Validators.is_status_valid(status):
            raise ValidationException(detail="无效的状态值")

        user = self.user_repository.get_by_id(user_id, tenant_id=tenant_id)
        if not user:
            raise NotFoundException(detail="用户不存在")

        user.status = status
        user.updated_by = updated_by

        updated_user = self.user_repository.update(user)

        logger.info(f"更新用户状态成功: {user.username}, 状态: {status}")

        return updated_user

    def update_user_avatar(self, user_id: int, avatar_path: str, tenant_id: int, updated_by: int) -> UserModel:
        """更新用户头像"""
        user = self.user_repository.get_by_id(user_id, tenant_id=tenant_id)
        if not user:
            raise NotFoundException(detail="用户不存在")

        user.avatar = avatar_path
        user.updated_by = updated_by

        updated_user = self.user_repository.update(user)

        logger.info(f"更新用户头像成功: {user.username}")

        return updated_user

    def get_user_roles(self, user_id: int, tenant_id: int) -> List[Dict[str, Any]]:
        """获取用户角色列表"""
        user = self.user_repository.get_by_id(user_id, tenant_id=tenant_id)
        if not user:
            raise NotFoundException(detail="用户不存在")

        user_roles = self.user_role_repository.get_by_user_id(user_id, tenant_id=tenant_id)

        roles = []
        for user_role in user_roles:
            role = user_role.role
            roles.append({
                "id": role.id,
                "name": role.name,
                "code": role.code,
                "type": role.type,
                "status": role.status,
                "is_primary": user_role.is_primary
            })

        return roles

    def assign_roles_to_user(self, user_id: int, role_ids: List[int], tenant_id: int, updated_by: int) -> bool:
        """分配角色给用户"""
        user = self.user_repository.get_by_id(user_id, tenant_id=tenant_id)
        if not user:
            raise NotFoundException(detail="用户不存在")

        if len(role_ids) > 10:
            raise ValidationException(detail="用户最多可分配10个角色")

        from App.Repositories.RoleRepository import RoleRepository
        role_repository = RoleRepository(self.db)

        for role_id in role_ids:
            role = role_repository.get_by_id(role_id, tenant_id=tenant_id)
            if not role:
                raise ValidationException(detail=f"角色ID {role_id} 不存在")

        self.user_role_repository.batch_assign_roles(user_id, role_ids, tenant_id=tenant_id, operator_id=updated_by)

        logger.info(f"分配角色给用户成功: {user.username}")

        return True

    def set_primary_role(self, user_id: int, role_id: int, tenant_id: int, updated_by: int) -> bool:
        """设置用户主角色"""
        user = self.user_repository.get_by_id(user_id, tenant_id=tenant_id)
        if not user:
            raise NotFoundException(detail="用户不存在")

        from App.Repositories.RoleRepository import RoleRepository
        role_repository = RoleRepository(self.db)
        role = role_repository.get_by_id(role_id, tenant_id=tenant_id)
        if not role:
            raise ValidationException(detail=f"角色ID {role_id} 不存在")

        user_role = self.user_role_repository.get_by_user_and_role(user_id, role_id, tenant_id=tenant_id)
        if not user_role:
            raise ValidationException(detail="用户未关联该角色")

        user_roles = self.user_role_repository.get_by_user_id(user_id, tenant_id=tenant_id)
        for ur in user_roles:
            ur.is_primary = False
            self.user_role_repository.update(ur)

        user_role.is_primary = True
        user_role.updated_by = updated_by
        self.user_role_repository.update(user_role)

        logger.info(f"设置用户主角色成功: {user.username}, 角色: {role.name}")

        return True

    def reset_password(self, user_id: int, new_password: str, tenant_id: int, updated_by: int) -> bool:
        """重置用户密码"""
        user = self.user_repository.get_by_id(user_id, tenant_id=tenant_id)
        if not user:
            raise NotFoundException(detail="用户不存在")

        if not Validators.is_password_strong(new_password):
            raise ValidationException(detail="新密码强度不足")

        hashed_password = SecurityCore.get_password_hash(new_password)
        user.password = hashed_password
        user.updated_by = updated_by

        self.user_repository.update(user)

        logger.info(f"用户 {user.username} 密码重置成功")

        return True
