"""Authentication Service"""

from datetime import datetime
from typing import Dict, Any
from sqlalchemy.orm import Session
from App.Models.User import UserModel
from App.Core.Security import SecurityCore
from App.Core.Exceptions import AuthenticationException, ValidationException
from App.Repositories.UserRepository import UserRepository
from App.Utils.Validators import Validators
from App.Utils.Logger import logger


class AuthService:
    """认证服务类"""
    
    def __init__(self, db: Session):
        """初始化认证服务"""
        self.db = db
        self.user_repository = UserRepository(db)
    
    def login(self, username: str, password: str, ip: str = "") -> Dict[str, Any]:
        """用户登录"""
        if not Validators.is_username_valid(username):
            raise ValidationException(detail="用户名格式不正确")
        
        user = self.user_repository.get_by_username(username, include_deleted=False)
        if not user:
            raise AuthenticationException(detail="用户名或密码错误")
        
        if user.status != 1:
            raise AuthenticationException(detail="用户已被禁用")
        
        if not SecurityCore.verify_password(password, user.password):
            raise AuthenticationException(detail="用户名或密码错误")
        
        user.last_login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user.last_login_ip = ip
        self.user_repository.update(user)
        
        access_token = SecurityCore.create_access_token(
            data={"sub": str(user.id), "username": user.username, "tenant_id": user.tenant_id}
        )
        
        refresh_token = SecurityCore.create_refresh_token(
            data={"sub": str(user.id), "username": user.username, "tenant_id": user.tenant_id}
        )
        
        logger.info(f"用户 {username} 登录成功，IP: {ip}")
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "nickname": user.nickname,
                "email": user.email,
                "phone": user.phone,
                "avatar": user.avatar,
                "department_id": user.department_id,
                "tenant_id": user.tenant_id,
                "status": user.status
            }
        }
    
    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """刷新Token"""
        payload = SecurityCore.verify_token(refresh_token)
        if not payload:
            raise AuthenticationException(detail="无效的刷新Token")
        
        if payload.get("token_type") != "refresh":
            raise AuthenticationException(detail="无效的Token类型")
        
        user_id = payload.get("sub")
        tenant_id = payload.get("tenant_id")
        user = self.user_repository.get_by_id(int(user_id), tenant_id=tenant_id, include_deleted=False)
        if not user:
            raise AuthenticationException(detail="用户不存在")
        
        if user.status != 1:
            raise AuthenticationException(detail="用户已被禁用")
        
        access_token = SecurityCore.create_access_token(
            data={"sub": str(user.id), "username": user.username, "tenant_id": user.tenant_id}
        )
        
        logger.info(f"用户 {user.username} 刷新Token成功")
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    
    def register(self, username: str, password: str, nickname: str, tenant_id: int, email: str = "", phone: str = "", created_by: int = None) -> UserModel:
        """用户注册"""
        if not Validators.is_username_valid(username):
            raise ValidationException(detail="用户名格式不正确")
        
        if not Validators.is_password_strong(password):
            raise ValidationException(detail="密码强度不足")
        
        existing_user = self.user_repository.get_by_username(username, tenant_id=tenant_id, include_deleted=False)
        if existing_user:
            raise ValidationException(detail="用户名已存在")
        
        if email:
            existing_user = self.user_repository.get_by_email(email, tenant_id=tenant_id, include_deleted=False)
            if existing_user:
                raise ValidationException(detail="邮箱已存在")
        
        if phone:
            existing_user = self.user_repository.get_by_phone(phone, tenant_id=tenant_id, include_deleted=False)
            if existing_user:
                raise ValidationException(detail="手机号已存在")
        
        hashed_password = SecurityCore.get_password_hash(password)
        
        user = UserModel(
            username=username,
            password=hashed_password,
            nickname=nickname,
            email=email,
            phone=phone,
            status=1,
            tenant_id=tenant_id,
            created_by=created_by,
            updated_by=created_by
        )
        
        created_user = self.user_repository.create(user)
        
        logger.info(f"用户 {username} 注册成功")
        
        return created_user
    
    def change_password(self, user_id: int, old_password: str, new_password: str, tenant_id: int) -> bool:
        """修改密码"""
        user = self.user_repository.get_by_id(user_id, tenant_id=tenant_id, include_deleted=False)
        if not user:
            raise AuthenticationException(detail="用户不存在")
        
        if not SecurityCore.verify_password(old_password, user.password):
            raise ValidationException(detail="旧密码错误")
        
        if not Validators.is_password_strong(new_password):
            raise ValidationException(detail="新密码强度不足")
        
        new_hashed_password = SecurityCore.get_password_hash(new_password)
        
        user.password = new_hashed_password
        self.user_repository.update(user)
        
        logger.info(f"用户 {user.username} 修改密码成功")
        
        return True
    
    def reset_password(self, user_id: int, new_password: str, tenant_id: int, updated_by: int = None) -> bool:
        """重置密码"""
        user = self.user_repository.get_by_id(user_id, tenant_id=tenant_id, include_deleted=False)
        if not user:
            raise AuthenticationException(detail="用户不存在")
        
        if not Validators.is_password_strong(new_password):
            raise ValidationException(detail="新密码强度不足")
        
        new_hashed_password = SecurityCore.get_password_hash(new_password)
        
        user.password = new_hashed_password
        if updated_by:
            user.updated_by = updated_by
        self.user_repository.update(user)
        
        logger.info(f"用户 {user.username} 密码重置成功")
        
        return True
