"""Dependencies Package"""

from App.Dependencies.Database import get_db
from App.Dependencies.Auth import get_current_user, get_current_user_id
from App.Dependencies.Permission import permission_dependency, get_user_permissions

__all__ = [
    "get_db",
    "get_current_user",
    "get_current_user_id",
    "permission_dependency",
    "get_user_permissions"
]