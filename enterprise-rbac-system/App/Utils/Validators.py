"""Validators"""

from typing import List
import re


class Validators:
    """验证工具类"""

    @staticmethod
    def is_email(email: str) -> bool:
        """验证邮箱格式"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    @staticmethod
    def is_phone(phone: str) -> bool:
        """验证手机号格式"""
        pattern = r"^1[3-9]\d{9}$"
        return bool(re.match(pattern, phone))

    @staticmethod
    def is_password_strong(password: str) -> bool:
        """验证密码强度（至少6位）"""
        return len(password) >= 6

    @staticmethod
    def is_username_valid(username: str) -> bool:
        """验证用户名格式（3-20位字母、数字、下划线）"""
        pattern = r"^[a-zA-Z0-9_]{3,20}$"
        return bool(re.match(pattern, username))

    @staticmethod
    def is_nickname_valid(nickname: str) -> bool:
        """验证昵称格式（2-20位）"""
        return 2 <= len(nickname) <= 20

    @staticmethod
    def is_department_code_valid(code: str) -> bool:
        """验证部门编码格式（2-50位字母、数字、下划线、中划线）"""
        pattern = r"^[a-zA-Z0-9_-]{2,50}$"
        return bool(re.match(pattern, code))

    @staticmethod
    def is_role_code_valid(code: str) -> bool:
        """验证角色编码格式（2-50位字母、数字、下划线）"""
        pattern = r"^[a-zA-Z0-9_]{2,50}$"
        return bool(re.match(pattern, code))

    @staticmethod
    def is_menu_code_valid(code: str) -> bool:
        """验证菜单编码格式（2-50位字母、数字、下划线）"""
        pattern = r"^[a-zA-Z0-9_]{2,50}$"
        return bool(re.match(pattern, code))

    @staticmethod
    def is_permission_code_valid(code: str) -> bool:
        """验证权限编码格式（2-50位字母、数字、下划线、冒号）"""
        pattern = r"^[a-zA-Z0-9_:]{2,50}$"
        return bool(re.match(pattern, code))

    @staticmethod
    def is_status_valid(status: int) -> bool:
        """验证状态值（0或1）"""
        return status in [0, 1]

    @staticmethod
    def is_level_valid(level: int) -> bool:
        """验证层级值（1-10）"""
        return 1 <= level <= 10

    @staticmethod
    def is_type_valid(type_value: int, valid_types: List[int]) -> bool:
        """验证类型值是否在有效范围内"""
        return type_value in valid_types
