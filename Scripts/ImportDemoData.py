"""
企业RBAC系统 - 详细演示数据导入脚本
功能：
1. 导入完整的企业级演示数据
2. 包含系统字典、配置、部门、菜单、权限、角色、用户、用户组等
3. 建立完整的关联关系
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from App.Config.Database import SessionLocal
from App.Core.Security import SecurityCore
from App.Models.User import UserModel
from App.Models.Role import RoleModel
from App.Models.UserRole import UserRoleModel
from App.Models.Department import DepartmentModel
from App.Models.Menu import MenuModel
from App.Models.Permission import PermissionModel
from App.Models.RolePermission import RolePermissionModel
from App.Models.MenuPermission import MenuPermissionModel
from App.Models.SystemDict import SystemDictModel
from App.Models.SystemDictItem import SystemDictItemModel
from App.Models.SystemConfig import SystemConfigModel
from App.Models.UserGroup import UserGroupModel
from App.Models.UserGroupRelation import UserGroupRelationModel
from App.Models.UserGroupRoleRelation import UserGroupRoleRelationModel
from App.Models.UserProfile import UserProfileModel

security = SecurityCore()


def init_system_dicts(db):
    """初始化系统字典"""
    print("正在初始化系统字典...")
    
    dicts = [
        {
            "code": "gender",
            "name": "性别",
            "description": "用户性别",
            "items": [
                {"label": "男", "value": "1", "color": "#1890ff", "sort": 1},
                {"label": "女", "value": "2", "color": "#eb2f96", "sort": 2},
                {"label": "未知", "value": "0", "color": "#8c8c8c", "sort": 3}
            ]
        },
        {
            "code": "status",
            "name": "状态",
            "description": "通用状态",
            "items": [
                {"label": "启用", "value": "1", "color": "#52c41a", "sort": 1},
                {"label": "禁用", "value": "0", "color": "#ff4d4f", "sort": 2}
            ]
        },
        {
            "code": "user_type",
            "name": "用户类型",
            "description": "用户类型",
            "items": [
                {"label": "系统用户", "value": "0", "color": "#1890ff", "sort": 1},
                {"label": "普通用户", "value": "1", "color": "#52c41a", "sort": 2},
                {"label": "测试用户", "value": "2", "color": "#faad14", "sort": 3}
            ]
        },
        {
            "code": "data_scope",
            "name": "数据范围",
            "description": "角色数据权限范围",
            "items": [
                {"label": "全部数据", "value": "0", "color": "#1890ff", "sort": 1},
                {"label": "本部门数据", "value": "1", "color": "#52c41a", "sort": 2},
                {"label": "本部门及下级", "value": "2", "color": "#faad14", "sort": 3},
                {"label": "仅本人数据", "value": "3", "color": "#ff4d4f", "sort": 4},
                {"label": "自定义数据", "value": "4", "color": "#722ed1", "sort": 5}
            ]
        },
        {
            "code": "permission_type",
            "name": "权限类型",
            "description": "权限类型",
            "items": [
                {"label": "菜单", "value": "0", "color": "#1890ff", "sort": 1},
                {"label": "按钮", "value": "1", "color": "#52c41a", "sort": 2},
                {"label": "API", "value": "2", "color": "#faad14", "sort": 3},
                {"label": "数据", "value": "3", "color": "#ff4d4f", "sort": 4},
                {"label": "字段", "value": "4", "color": "#722ed1", "sort": 5}
            ]
        },
        {
            "code": "menu_type",
            "name": "菜单类型",
            "description": "菜单类型",
            "items": [
                {"label": "目录", "value": "0", "color": "#1890ff", "sort": 1},
                {"label": "菜单", "value": "1", "color": "#52c41a", "sort": 2},
                {"label": "按钮", "value": "2", "color": "#faad14", "sort": 3}
            ]
        }
    ]
    
    for dict_data in dicts:
        sys_dict = SystemDictModel(
            code=dict_data["code"],
            name=dict_data["name"],
            description=dict_data["description"],
            tenant_id=1,
            status=1,
            sort=0
        )
        db.add(sys_dict)
        db.flush()
        
        for item_data in dict_data["items"]:
            item = SystemDictItemModel(
                dict_id=sys_dict.id,
                label=item_data["label"],
                value=item_data["value"],
                color=item_data.get("color"),
                sort=item_data["sort"],
                tenant_id=1,
                status=1
            )
            db.add(item)
    
    db.commit()
    print(f"[OK] 系统字典初始化完成，共 {len(dicts)} 个字典")


def init_system_configs(db):
    """初始化系统配置"""
    print("正在初始化系统配置...")
    
    configs = [
        {
            "config_key": "site_name",
            "config_value": "企业级RBAC系统",
            "config_type": "string",
            "group_name": "基本设置",
            "description": "网站名称",
            "is_system": 1,
            "sort": 1
        },
        {
            "config_key": "site_description",
            "config_value": "基于Python FastAPI构建的企业级权限管理系统",
            "config_type": "string",
            "group_name": "基本设置",
            "description": "网站描述",
            "is_system": 1,
            "sort": 2
        },
        {
            "config_key": "register_enabled",
            "config_value": "1",
            "config_type": "bool",
            "group_name": "用户设置",
            "description": "是否开启用户注册",
            "is_system": 0,
            "sort": 1
        },
        {
            "config_key": "password_min_length",
            "config_value": "6",
            "config_type": "int",
            "group_name": "用户设置",
            "description": "密码最小长度",
            "is_system": 0,
            "sort": 2
        },
        {
            "config_key": "session_timeout",
            "config_value": "7200",
            "config_type": "int",
            "group_name": "安全设置",
            "description": "会话超时时间(秒)",
            "is_system": 1,
            "sort": 1
        },
        {
            "config_key": "login_max_attempts",
            "config_value": "5",
            "config_type": "int",
            "group_name": "安全设置",
            "description": "最大登录失败次数",
            "is_system": 0,
            "sort": 2
        },
        {
            "config_key": "copyright",
            "config_value": "© 2026 Enterprise RBAC System",
            "config_type": "string",
            "group_name": "基本设置",
            "description": "版权信息",
            "is_system": 0,
            "sort": 3
        }
    ]
    
    for config_data in configs:
        config = SystemConfigModel(
            config_key=config_data["config_key"],
            config_value=config_data["config_value"],
            config_type=config_data["config_type"],
            group_name=config_data["group_name"],
            description=config_data["description"],
            is_system=config_data["is_system"],
            sort=config_data["sort"],
            tenant_id=1,
            status=1
        )
        db.add(config)
    
    db.commit()
    print(f"[OK] 系统配置初始化完成，共 {len(configs)} 个配置")


def init_departments(db):
    """初始化部门数据"""
    print("正在初始化部门数据...")
    
    departments = [
        {
            "name": "总公司",
            "code": "HQ",
            "description": "集团总公司",
            "level": 1,
            "children": [
                {
                    "name": "技术部",
                    "code": "TECH",
                    "description": "技术研发部门",
                    "level": 2,
                    "children": [
                        {"name": "前端组", "code": "FRONTEND", "description": "前端开发组", "level": 3},
                        {"name": "后端组", "code": "BACKEND", "description": "后端开发组", "level": 3},
                        {"name": "测试组", "code": "TEST", "description": "质量测试组", "level": 3}
                    ]
                },
                {
                    "name": "市场部",
                    "code": "MARKET",
                    "description": "市场营销部门",
                    "level": 2,
                    "children": [
                        {"name": "销售组", "code": "SALES", "description": "产品销售组", "level": 3},
                        {"name": "运营组", "code": "OPERATION", "description": "市场运营组", "level": 3}
                    ]
                },
                {
                    "name": "人事部",
                    "code": "HR",
                    "description": "人力资源部门",
                    "level": 2
                },
                {
                    "name": "财务部",
                    "code": "FINANCE",
                    "description": "财务部门",
                    "level": 2
                }
            ]
        }
    ]
    
    def create_dept(dept_data, parent_id=None):
        dept = DepartmentModel(
            name=dept_data["name"],
            code=dept_data["code"],
            description=dept_data["description"],
            parent_id=parent_id,
            level=dept_data["level"],
            tenant_id=1,
            status=1
        )
        db.add(dept)
        db.flush()
        
        if "children" in dept_data:
            for child in dept_data["children"]:
                create_dept(child, dept.id)
    
    for dept in departments:
        create_dept(dept)
    
    db.commit()
    print("[OK] 部门数据初始化完成")


def init_menus(db):
    """初始化菜单数据"""
    print("正在初始化菜单数据...")
    
    menus = [
        {
            "name": "首页",
            "code": "dashboard",
            "type": 0,
            "path": "/dashboard",
            "icon": "HomeOutlined",
            "sort": 1,
            "level": 1
        },
        {
            "name": "系统管理",
            "code": "system",
            "type": 0,
            "path": "/system",
            "icon": "SettingOutlined",
            "sort": 2,
            "level": 1,
            "children": [
                {
                    "name": "用户管理",
                    "code": "user",
                    "type": 0,
                    "path": "/system/user",
                    "icon": "UserOutlined",
                    "sort": 1,
                    "level": 2
                },
                {
                    "name": "角色管理",
                    "code": "role",
                    "type": 0,
                    "path": "/system/role",
                    "icon": "TeamOutlined",
                    "sort": 2,
                    "level": 2
                },
                {
                    "name": "菜单管理",
                    "code": "menu",
                    "type": 0,
                    "path": "/system/menu",
                    "icon": "MenuOutlined",
                    "sort": 3,
                    "level": 2
                },
                {
                    "name": "部门管理",
                    "code": "department",
                    "type": 0,
                    "path": "/system/department",
                    "icon": "ApartmentOutlined",
                    "sort": 4,
                    "level": 2
                },
                {
                    "name": "用户组管理",
                    "code": "user-group",
                    "type": 0,
                    "path": "/system/user-group",
                    "icon": "UsergroupAddOutlined",
                    "sort": 5,
                    "level": 2
                },
                {
                    "name": "系统字典",
                    "code": "dict",
                    "type": 0,
                    "path": "/system/dict",
                    "icon": "BookOutlined",
                    "sort": 6,
                    "level": 2
                },
                {
                    "name": "系统配置",
                    "code": "config",
                    "type": 0,
                    "path": "/system/config",
                    "icon": "ControlOutlined",
                    "sort": 7,
                    "level": 2
                }
            ]
        },
        {
            "name": "日志管理",
            "code": "log",
            "type": 0,
            "path": "/log",
            "icon": "FileTextOutlined",
            "sort": 3,
            "level": 1,
            "children": [
                {
                    "name": "操作日志",
                    "code": "operation-log",
                    "type": 0,
                    "path": "/log/operation",
                    "icon": "FileTextOutlined",
                    "sort": 1,
                    "level": 2
                },
                {
                    "name": "审计日志",
                    "code": "audit-log",
                    "type": 0,
                    "path": "/log/audit",
                    "icon": "AuditOutlined",
                    "sort": 2,
                    "level": 2
                }
            ]
        },
        {
            "name": "个人中心",
            "code": "personal",
            "type": 0,
            "path": "/personal",
            "icon": "UserOutlined",
            "sort": 4,
            "level": 1
        }
    ]
    
    def create_menu(menu_data, parent_id=None):
        menu = MenuModel(
            name=menu_data["name"],
            code=menu_data["code"],
            type=menu_data["type"],
            path=menu_data.get("path"),
            icon=menu_data.get("icon"),
            parent_id=parent_id,
            level=menu_data["level"],
            sort=menu_data["sort"],
            tenant_id=1,
            status=1
        )
        db.add(menu)
        db.flush()
        
        if "children" in menu_data:
            for child in menu_data["children"]:
                create_menu(child, menu.id)
    
    for menu in menus:
        create_menu(menu)
    
    db.commit()
    print("[OK] 菜单数据初始化完成")


def init_permissions(db):
    """初始化权限数据"""
    print("正在初始化权限数据...")
    
    permissions = [
        {"name": "用户查看", "code": "user:view", "type": 2, "resource_type": "user", "action": "view", "path": "/api/v1/users", "method": "GET"},
        {"name": "用户创建", "code": "user:create", "type": 2, "resource_type": "user", "action": "create", "path": "/api/v1/users", "method": "POST"},
        {"name": "用户更新", "code": "user:update", "type": 2, "resource_type": "user", "action": "update", "path": "/api/v1/users/*", "method": "PUT"},
        {"name": "用户删除", "code": "user:delete", "type": 2, "resource_type": "user", "action": "delete", "path": "/api/v1/users/*", "method": "DELETE"},
        
        {"name": "角色查看", "code": "role:view", "type": 2, "resource_type": "role", "action": "view", "path": "/api/v1/roles", "method": "GET"},
        {"name": "角色创建", "code": "role:create", "type": 2, "resource_type": "role", "action": "create", "path": "/api/v1/roles", "method": "POST"},
        {"name": "角色更新", "code": "role:update", "type": 2, "resource_type": "role", "action": "update", "path": "/api/v1/roles/*", "method": "PUT"},
        {"name": "角色删除", "code": "role:delete", "type": 2, "resource_type": "role", "action": "delete", "path": "/api/v1/roles/*", "method": "DELETE"},
        
        {"name": "菜单查看", "code": "menu:view", "type": 2, "resource_type": "menu", "action": "view", "path": "/api/v1/menus", "method": "GET"},
        {"name": "菜单创建", "code": "menu:create", "type": 2, "resource_type": "menu", "action": "create", "path": "/api/v1/menus", "method": "POST"},
        {"name": "菜单更新", "code": "menu:update", "type": 2, "resource_type": "menu", "action": "update", "path": "/api/v1/menus/*", "method": "PUT"},
        {"name": "菜单删除", "code": "menu:delete", "type": 2, "resource_type": "menu", "action": "delete", "path": "/api/v1/menus/*", "method": "DELETE"},
        
        {"name": "部门查看", "code": "department:view", "type": 2, "resource_type": "department", "action": "view", "path": "/api/v1/departments", "method": "GET"},
        {"name": "部门创建", "code": "department:create", "type": 2, "resource_type": "department", "action": "create", "path": "/api/v1/departments", "method": "POST"},
        {"name": "部门更新", "code": "department:update", "type": 2, "resource_type": "department", "action": "update", "path": "/api/v1/departments/*", "method": "PUT"},
        {"name": "部门删除", "code": "department:delete", "type": 2, "resource_type": "department", "action": "delete", "path": "/api/v1/departments/*", "method": "DELETE"},
        
        {"name": "用户组查看", "code": "user-group:view", "type": 2, "resource_type": "user-group", "action": "view", "path": "/api/v1/user-groups", "method": "GET"},
        {"name": "用户组创建", "code": "user-group:create", "type": 2, "resource_type": "user-group", "action": "create", "path": "/api/v1/user-groups", "method": "POST"},
        {"name": "用户组更新", "code": "user-group:update", "type": 2, "resource_type": "user-group", "action": "update", "path": "/api/v1/user-groups/*", "method": "PUT"},
        {"name": "用户组删除", "code": "user-group:delete", "type": 2, "resource_type": "user-group", "action": "delete", "path": "/api/v1/user-groups/*", "method": "DELETE"},
        
        {"name": "字典查看", "code": "dict:view", "type": 2, "resource_type": "dict", "action": "view", "path": "/api/v1/system-dicts", "method": "GET"},
        {"name": "字典创建", "code": "dict:create", "type": 2, "resource_type": "dict", "action": "create", "path": "/api/v1/system-dicts", "method": "POST"},
        {"name": "字典更新", "code": "dict:update", "type": 2, "resource_type": "dict", "action": "update", "path": "/api/v1/system-dicts/*", "method": "PUT"},
        {"name": "字典删除", "code": "dict:delete", "type": 2, "resource_type": "dict", "action": "delete", "path": "/api/v1/system-dicts/*", "method": "DELETE"},
        
        {"name": "配置查看", "code": "config:view", "type": 2, "resource_type": "config", "action": "view", "path": "/api/v1/system-configs", "method": "GET"},
        {"name": "配置创建", "code": "config:create", "type": 2, "resource_type": "config", "action": "create", "path": "/api/v1/system-configs", "method": "POST"},
        {"name": "配置更新", "code": "config:update", "type": 2, "resource_type": "config", "action": "update", "path": "/api/v1/system-configs/*", "method": "PUT"},
        {"name": "配置删除", "code": "config:delete", "type": 2, "resource_type": "config", "action": "delete", "path": "/api/v1/system-configs/*", "method": "DELETE"},
        
        {"name": "操作日志查看", "code": "operation-log:view", "type": 2, "resource_type": "operation-log", "action": "view", "path": "/api/v1/operation-logs", "method": "GET"},
        {"name": "审计日志查看", "code": "audit-log:view", "type": 2, "resource_type": "audit-log", "action": "view", "path": "/api/v1/audit-logs", "method": "GET"},
        {"name": "权限查看", "code": "permission:view", "type": 2, "resource_type": "permission", "action": "view", "path": "/api/v1/permissions", "method": "GET"}
    ]
    
    for perm_data in permissions:
        perm = PermissionModel(
            name=perm_data["name"],
            code=perm_data["code"],
            type=perm_data["type"],
            resource_type=perm_data["resource_type"],
            action=perm_data["action"],
            path=perm_data.get("path"),
            method=perm_data.get("method"),
            level=1,
            tenant_id=1,
            status=1
        )
        db.add(perm)
    
    db.commit()
    print(f"[OK] 权限数据初始化完成，共 {len(permissions)} 个权限")


def init_roles(db):
    """初始化角色数据"""
    print("正在初始化角色数据...")
    
    roles = [
        {
            "name": "超级管理员",
            "code": "super_admin",
            "type": 0,
            "data_scope": 0,
            "sort": 1,
            "description": "系统超级管理员，拥有所有权限"
        },
        {
            "name": "系统管理员",
            "code": "admin",
            "type": 1,
            "data_scope": 0,
            "sort": 2,
            "description": "系统管理员，管理系统配置"
        },
        {
            "name": "部门经理",
            "code": "manager",
            "type": 2,
            "data_scope": 2,
            "sort": 3,
            "description": "部门经理，管理本部门及下级数据"
        },
        {
            "name": "普通员工",
            "code": "staff",
            "type": 3,
            "data_scope": 3,
            "sort": 4,
            "description": "普通员工，只能查看和编辑本人数据"
        }
    ]
    
    role_objects = []
    for role_data in roles:
        role = RoleModel(
            name=role_data["name"],
            code=role_data["code"],
            type=role_data["type"],
            data_scope=role_data["data_scope"],
            sort=role_data["sort"],
            description=role_data["description"],
            level=1,
            tenant_id=1,
            status=1
        )
        db.add(role)
        role_objects.append(role)
    
    db.commit()
    print(f"[OK] 角色数据初始化完成，共 {len(roles)} 个角色")
    return role_objects


def init_user_groups(db):
    """初始化用户组数据"""
    print("正在初始化用户组数据...")
    
    user_groups = [
        {
            "name": "技术团队",
            "code": "tech_team",
            "description": "技术部全体成员",
            "sort": 1
        },
        {
            "name": "市场团队",
            "code": "market_team",
            "description": "市场部全体成员",
            "sort": 2
        },
        {
            "name": "管理团队",
            "code": "management_team",
            "description": "公司管理层",
            "sort": 3
        },
        {
            "name": "前端开发组",
            "code": "frontend_team",
            "description": "前端开发团队",
            "sort": 4
        },
        {
            "name": "后端开发组",
            "code": "backend_team",
            "description": "后端开发团队",
            "sort": 5
        }
    ]
    
    group_objects = []
    for group_data in user_groups:
        group = UserGroupModel(
            name=group_data["name"],
            code=group_data["code"],
            description=group_data["description"],
            sort=group_data["sort"],
            tenant_id=1,
            status=1
        )
        db.add(group)
        group_objects.append(group)
    
    db.commit()
    print(f"[OK] 用户组数据初始化完成，共 {len(user_groups)} 个用户组")
    return group_objects


def init_users(db, roles, user_groups):
    """初始化用户数据"""
    print("正在初始化用户数据...")
    
    hq_dept = db.query(DepartmentModel).filter(DepartmentModel.code == "HQ", DepartmentModel.tenant_id == 1).first()
    tech_dept = db.query(DepartmentModel).filter(DepartmentModel.code == "TECH", DepartmentModel.tenant_id == 1).first()
    market_dept = db.query(DepartmentModel).filter(DepartmentModel.code == "MARKET", DepartmentModel.tenant_id == 1).first()
    frontend_dept = db.query(DepartmentModel).filter(DepartmentModel.code == "FRONTEND", DepartmentModel.tenant_id == 1).first()
    backend_dept = db.query(DepartmentModel).filter(DepartmentModel.code == "BACKEND", DepartmentModel.tenant_id == 1).first()
    
    all_permissions = db.query(PermissionModel).filter(PermissionModel.tenant_id == 1).all()
    assigned_role_ids = set()
    assigned_group_role_ids = set()
    
    users_data = [
        {
            "username": "admin",
            "password": "admin123",
            "nickname": "系统管理员",
            "email": "admin@example.com",
            "phone": "13800138000",
            "department_id": hq_dept.id if hq_dept else None,
            "role_codes": ["super_admin"],
            "group_codes": ["management_team"],
            "profile": {"gender": "1"}
        },
        {
            "username": "zhangsan",
            "password": "123456",
            "nickname": "张三",
            "email": "zhangsan@example.com",
            "phone": "13800138001",
            "department_id": tech_dept.id if tech_dept else None,
            "role_codes": ["admin"],
            "group_codes": ["tech_team", "backend_team"],
            "profile": {"gender": "1"}
        },
        {
            "username": "lisi",
            "password": "123456",
            "nickname": "李四",
            "email": "lisi@example.com",
            "phone": "13800138002",
            "department_id": market_dept.id if market_dept else None,
            "role_codes": ["manager"],
            "group_codes": ["market_team"],
            "profile": {"gender": "2"}
        },
        {
            "username": "wangwu",
            "password": "123456",
            "nickname": "王五",
            "email": "wangwu@example.com",
            "phone": "13800138003",
            "department_id": frontend_dept.id if frontend_dept else None,
            "role_codes": ["staff"],
            "group_codes": ["tech_team", "frontend_team"],
            "profile": {"gender": "1"}
        },
        {
            "username": "zhaoliu",
            "password": "123456",
            "nickname": "赵六",
            "email": "zhaoliu@example.com",
            "phone": "13800138004",
            "department_id": backend_dept.id if backend_dept else None,
            "role_codes": ["staff"],
            "group_codes": ["tech_team", "backend_team"],
            "profile": {"gender": "1"}
        },
        {
            "username": "qianqi",
            "password": "123456",
            "nickname": "钱七",
            "email": "qianqi@example.com",
            "phone": "13800138005",
            "department_id": market_dept.id if market_dept else None,
            "role_codes": ["staff"],
            "group_codes": ["market_team"],
            "profile": {"gender": "2"}
        }
    ]
    
    user_objects = []
    for user_data in users_data:
        user = UserModel(
            username=user_data["username"],
            password=security.get_password_hash(user_data["password"]),
            nickname=user_data["nickname"],
            email=user_data["email"],
            phone=user_data["phone"],
            department_id=user_data["department_id"],
            tenant_id=1,
            status=1
        )
        db.add(user)
        db.flush()
        user_objects.append(user)
        
        profile = UserProfileModel(
            user_id=user.id,
            gender=user_data["profile"].get("gender"),
            tenant_id=1
        )
        db.add(profile)
        
        for role_code in user_data["role_codes"]:
            role = next((r for r in roles if r.code == role_code), None)
            if role:
                user_role = UserRoleModel(
                    user_id=user.id,
                    role_id=role.id,
                    is_primary=(role_code == user_data["role_codes"][0]),
                    tenant_id=1
                )
                db.add(user_role)
                
                if role.id not in assigned_role_ids:
                    for perm in all_permissions:
                        role_perm = RolePermissionModel(
                            role_id=role.id,
                            permission_id=perm.id,
                            tenant_id=1
                        )
                        db.add(role_perm)
                    assigned_role_ids.add(role.id)
        
        for group_code in user_data["group_codes"]:
            group = next((g for g in user_groups if g.code == group_code), None)
            if group:
                user_group_rel = UserGroupRelationModel(
                    user_id=user.id,
                    user_group_id=group.id,
                    tenant_id=1
                )
                db.add(user_group_rel)
                
                for role_code in user_data["role_codes"]:
                    role = next((r for r in roles if r.code == role_code), None)
                    key = (group.id, role.id)
                    if role and key not in assigned_group_role_ids:
                        group_role_rel = UserGroupRoleRelationModel(
                            user_group_id=group.id,
                            role_id=role.id,
                            tenant_id=1
                        )
                        db.add(group_role_rel)
                        assigned_group_role_ids.add(key)
    
    db.commit()
    print(f"[OK] 用户数据初始化完成，共 {len(users_data)} 个用户")
    return user_objects


def main():
    print("=" * 70)
    print("企业RBAC系统 - 详细演示数据导入脚本")
    print("=" * 70)
    
    db = SessionLocal()
    try:
        init_system_dicts(db)
        init_system_configs(db)
        init_departments(db)
        init_menus(db)
        init_permissions(db)
        roles = init_roles(db)
        user_groups = init_user_groups(db)
        init_users(db, roles, user_groups)
        
        print("\n" + "=" * 70)
        print("[OK] 演示数据导入成功完成！")
        print("=" * 70)
        print("\n默认账号信息：")
        print("  用户名: admin")
        print("  密码: admin123")
        print("\n测试用户:")
        print("  zhangsan/123456")
        print("  lisi/123456")
        print("  wangwu/123456")
        print("  zhaoliu/123456")
        print("  qianqi/123456")
        
    except Exception as e:
        print(f"\n[FAIL] 演示数据导入失败: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
