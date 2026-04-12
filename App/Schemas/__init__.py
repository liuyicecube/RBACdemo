"""Schemas Package"""

from App.Schemas.Base import (
    BaseSchema,
    BaseCreateSchema,
    BaseUpdateSchema,
    BaseResponse,
    PaginationResponse
)
from App.Schemas.Auth import (
    LoginRequest,
    RegisterRequest,
    RefreshTokenRequest,
    ChangePasswordRequest,
    ResetPasswordRequest,
    TokenResponse,
    UserInfoResponse,
    LoginResponse,
    AuthResponse
)
from App.Schemas.User import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserListResponse,
    UserRoleResponse,
    UserRolesResponse,
    AssignRolesRequest,
    SetPrimaryRoleRequest,
    UserFilter
)
from App.Schemas.Role import (
    RoleBase,
    RoleCreate,
    RoleUpdate,
    RoleResponse,
    RoleListResponse,
    RolePermissionResponse,
    RolePermissionsResponse,
    AssignPermissionsRequest,
    RoleFilter
)
from App.Schemas.Permission import (
    PermissionBase,
    PermissionCreate,
    PermissionUpdate,
    PermissionResponse,
    PermissionListResponse,
    PermissionRoleResponse,
    PermissionRolesResponse,
    PermissionFilter
)
from App.Schemas.Department import (
    DepartmentBase,
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
    DepartmentListResponse,
    DepartmentTreeResponse,
    DepartmentFilter
)
from App.Schemas.Menu import (
    MenuBase,
    MenuCreate,
    MenuUpdate,
    MenuResponse,
    MenuListResponse,
    MenuTreeResponse,
    MenuFilter
)

__all__ = [
    # Base
    "BaseSchema",
    "BaseCreateSchema",
    "BaseUpdateSchema",
    "BaseResponse",
    "PaginationResponse",

    # Auth
    "LoginRequest",
    "RegisterRequest",
    "RefreshTokenRequest",
    "ChangePasswordRequest",
    "ResetPasswordRequest",
    "TokenResponse",
    "UserInfoResponse",
    "LoginResponse",
    "AuthResponse",

    # User
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserListResponse",
    "UserRoleResponse",
    "UserRolesResponse",
    "AssignRolesRequest",
    "SetPrimaryRoleRequest",
    "UserFilter",

    # Role
    "RoleBase",
    "RoleCreate",
    "RoleUpdate",
    "RoleResponse",
    "RoleListResponse",
    "RolePermissionResponse",
    "RolePermissionsResponse",
    "AssignPermissionsRequest",
    "RoleFilter",

    # Permission
    "PermissionBase",
    "PermissionCreate",
    "PermissionUpdate",
    "PermissionResponse",
    "PermissionListResponse",
    "PermissionRoleResponse",
    "PermissionRolesResponse",
    "PermissionFilter",

    # Department
    "DepartmentBase",
    "DepartmentCreate",
    "DepartmentUpdate",
    "DepartmentResponse",
    "DepartmentListResponse",
    "DepartmentTreeResponse",
    "DepartmentFilter",

    # Menu
    "MenuBase",
    "MenuCreate",
    "MenuUpdate",
    "MenuResponse",
    "MenuListResponse",
    "MenuTreeResponse",
    "MenuFilter"
]
