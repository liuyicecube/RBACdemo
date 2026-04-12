"""User Profile Service"""

from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from App.Models.UserProfile import UserProfileModel
from App.Core.Exceptions import ValidationException, NotFoundException
from App.Repositories.UserProfileRepository import UserProfileRepository
from App.Utils.Logger import logger


class UserProfileService:
    """用户资料服务类"""

    def __init__(self, db: Session):
        """初始化用户资料服务"""
        self.db = db
        self.user_profile_repository = UserProfileRepository(db)
        from App.Repositories.UserRepository import UserRepository
        self.user_repository = UserRepository(db)

    def get_profile_by_id(self, profile_id: int, tenant_id: int) -> UserProfileModel:
        """根据ID获取用户资料"""
        profile = self.user_profile_repository.get_by_id(profile_id, tenant_id=tenant_id)
        if not profile:
            raise NotFoundException(detail="用户资料不存在")
        return profile

    def get_profile_by_user_id(self, user_id: int, tenant_id: int) -> Optional[UserProfileModel]:
        """根据用户ID获取用户资料"""
        user = self.user_repository.get_by_id(user_id, tenant_id=tenant_id)
        if not user:
            raise NotFoundException(detail="用户不存在")

        return self.user_profile_repository.get_by_user_id(user_id, tenant_id=tenant_id)

    def get_or_create_profile(self, user_id: int, tenant_id: int, operator_id: int) -> UserProfileModel:
        """获取或创建用户资料"""
        profile = self.user_profile_repository.get_by_user_id(user_id, tenant_id=tenant_id)

        if not profile:
            user = self.user_repository.get_by_id(user_id, tenant_id=tenant_id)
            if not user:
                raise NotFoundException(detail="用户不存在")

            profile = UserProfileModel(
                user_id=user_id,
                tenant_id=tenant_id,
                created_by=operator_id,
                updated_by=operator_id
            )
            profile = self.user_profile_repository.create(profile)

        return profile

    def create_profile(self, profile_data: Dict[str, Any], tenant_id: int, created_by: int) -> UserProfileModel:
        """创建用户资料"""
        user_id = profile_data.get("user_id")
        user = self.user_repository.get_by_id(user_id, tenant_id=tenant_id)
        if not user:
            raise NotFoundException(detail="用户不存在")

        existing_profile = self.user_profile_repository.get_by_user_id(user_id, tenant_id=tenant_id)
        if existing_profile:
            raise ValidationException(detail="该用户已有资料，请使用更新接口")

        profile = UserProfileModel(
            user_id=user_id,
            gender=profile_data.get("gender"),
            birthday=profile_data.get("birthday"),
            id_card=profile_data.get("id_card"),
            address=profile_data.get("address"),
            emergency_contact=profile_data.get("emergency_contact"),
            emergency_phone=profile_data.get("emergency_phone"),
            position=profile_data.get("position"),
            entry_date=profile_data.get("entry_date"),
            remark=profile_data.get("remark"),
            tenant_id=tenant_id,
            created_by=created_by,
            updated_by=created_by
        )

        created_profile = self.user_profile_repository.create(profile)

        logger.info(f"创建用户资料成功: 用户ID={user_id}")

        return created_profile

    def update_profile(self, user_id: int, profile_data: Dict[str, Any], tenant_id: int, updated_by: int) -> UserProfileModel:
        """更新用户资料"""
        user = self.user_repository.get_by_id(user_id, tenant_id=tenant_id)
        if not user:
            raise NotFoundException(detail="用户不存在")

        profile = self.user_profile_repository.get_by_user_id(user_id, tenant_id=tenant_id)

        if not profile:
            profile = UserProfileModel(
                user_id=user_id,
                tenant_id=tenant_id,
                created_by=updated_by,
                updated_by=updated_by
            )
            profile = self.user_profile_repository.create(profile)

        if "gender" in profile_data:
            profile.gender = profile_data.get("gender")

        if "birthday" in profile_data:
            profile.birthday = profile_data.get("birthday")

        if "id_card" in profile_data:
            profile.id_card = profile_data.get("id_card")

        if "address" in profile_data:
            profile.address = profile_data.get("address")

        if "emergency_contact" in profile_data:
            profile.emergency_contact = profile_data.get("emergency_contact")

        if "emergency_phone" in profile_data:
            profile.emergency_phone = profile_data.get("emergency_phone")

        if "position" in profile_data:
            profile.position = profile_data.get("position")

        if "entry_date" in profile_data:
            profile.entry_date = profile_data.get("entry_date")

        if "remark" in profile_data:
            profile.remark = profile_data.get("remark")

        profile.updated_by = updated_by

        updated_profile = self.user_profile_repository.update(profile)

        logger.info(f"更新用户资料成功: 用户ID={user_id}")

        return updated_profile

    def delete_profile(self, profile_id: int, tenant_id: int) -> bool:
        """删除用户资料"""
        profile = self.user_profile_repository.get_by_id(profile_id, tenant_id=tenant_id)
        if not profile:
            raise NotFoundException(detail="用户资料不存在")

        self.user_profile_repository.delete(profile)

        logger.info(f"删除用户资料成功: 资料ID={profile_id}")

        return True

    def delete_profile_by_user_id(self, user_id: int, tenant_id: int) -> bool:
        """根据用户ID删除用户资料"""
        user = self.user_repository.get_by_id(user_id, tenant_id=tenant_id)
        if not user:
            raise NotFoundException(detail="用户不存在")

        success = self.user_profile_repository.delete_by_user_id(user_id, tenant_id=tenant_id)

        if success:
            logger.info(f"删除用户资料成功: 用户ID={user_id}")

        return success
