"""
生成SQL迁移脚本
功能：
1. 生成数据库表结构SQL
2. 生成演示数据SQL
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from App.Config.Database import Base, engine
from App.Models.User import UserModel
from App.Models.Role import RoleModel
from App.Models.Permission import PermissionModel
from App.Models.Department import DepartmentModel
from App.Models.Menu import MenuModel
from App.Models.UserRole import UserRoleModel
from App.Models.RolePermission import RolePermissionModel
from App.Models.DataPermissionRule import DataPermissionRuleModel
from App.Models.OperationLog import OperationLogModel
from App.Models.UserSession import UserSessionModel
from App.Models.AuditLog import AuditLogModel
from App.Models.SystemDict import SystemDictModel
from App.Models.SystemDictItem import SystemDictItemModel
from App.Models.UserGroup import UserGroupModel
from App.Models.UserGroupRelation import UserGroupRelationModel
from App.Models.UserGroupRoleRelation import UserGroupRoleRelationModel
from App.Models.MenuPermission import MenuPermissionModel
from App.Models.SystemConfig import SystemConfigModel
from App.Models.UserProfile import UserProfileModel
from sqlalchemy import create_engine, MetaData
from sqlalchemy.schema import CreateTable
from datetime import datetime
import pymysql
from App.Config.Settings import settings


def generate_schema_sql(output_file):
    """生成数据库表结构SQL"""
    print("正在生成数据库表结构SQL...")
    
    tables = [
        UserModel.__table__,
        RoleModel.__table__,
        PermissionModel.__table__,
        DepartmentModel.__table__,
        MenuModel.__table__,
        UserRoleModel.__table__,
        RolePermissionModel.__table__,
        DataPermissionRuleModel.__table__,
        OperationLogModel.__table__,
        UserSessionModel.__table__,
        AuditLogModel.__table__,
        SystemDictModel.__table__,
        SystemDictItemModel.__table__,
        UserGroupModel.__table__,
        UserGroupRelationModel.__table__,
        UserGroupRoleRelationModel.__table__,
        MenuPermissionModel.__table__,
        SystemConfigModel.__table__,
        UserProfileModel.__table__
    ]
    
    sql_content = "-- ============================================\n"
    sql_content += "-- 企业RBAC系统 - 数据库表结构\n"
    sql_content += f"-- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    sql_content += "-- ============================================\n\n"
    sql_content += "SET NAMES utf8mb4;\n"
    sql_content += "SET FOREIGN_KEY_CHECKS = 0;\n\n"
    
    for table in tables:
        sql_content += f"-- 表: {table.name}\n"
        sql_content += f"DROP TABLE IF EXISTS `{table.name}`;\n"
        create_stmt = str(CreateTable(table).compile(engine))
        sql_content += create_stmt
        sql_content += ";\n\n"
    
    sql_content += "SET FOREIGN_KEY_CHECKS = 1;\n"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(sql_content)
    
    print(f"[OK] 表结构SQL已生成: {output_file}")


def generate_demo_data_sql(output_file):
    """生成演示数据SQL"""
    print("正在生成演示数据SQL...")
    
    sql_content = "-- ============================================\n"
    sql_content += "-- 企业RBAC系统 - 演示数据\n"
    sql_content += f"-- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    sql_content += "-- ============================================\n\n"
    sql_content += "SET NAMES utf8mb4;\n"
    sql_content += "SET FOREIGN_KEY_CHECKS = 0;\n\n"
    
    sql_content += "-- ============================================\n"
    sql_content += "-- 1. 系统字典\n"
    sql_content += "-- ============================================\n\n"
    sql_content += "INSERT INTO `sys_dict` (`id`, `code`, `name`, `description`, `sort`, `tenant_id`, `status`, `created_at`, `updated_at`) VALUES\n"
    sql_content += "(1, 'gender', '性别', '用户性别', 0, 1, 1, NOW(), NOW()),\n"
    sql_content += "(2, 'status', '状态', '通用状态', 0, 1, 1, NOW(), NOW()),\n"
    sql_content += "(3, 'user_type', '用户类型', '用户类型', 0, 1, 1, NOW(), NOW()),\n"
    sql_content += "(4, 'data_scope', '数据范围', '角色数据权限范围', 0, 1, 1, NOW(), NOW()),\n"
    sql_content += "(5, 'permission_type', '权限类型', '权限类型', 0, 1, 1, NOW(), NOW()),\n"
    sql_content += "(6, 'menu_type', '菜单类型', '菜单类型', 0, 1, 1, NOW(), NOW());\n\n"
    
    sql_content += "INSERT INTO `sys_dict_item` (`id`, `dict_id`, `label`, `value`, `color`, `sort`, `tenant_id`, `status`, `created_at`, `updated_at`) VALUES\n"
    sql_content += "(1, 1, '男', '1', '#1890ff', 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(2, 1, '女', '2', '#eb2f96', 2, 1, 1, NOW(), NOW()),\n"
    sql_content += "(3, 1, '未知', '0', '#8c8c8c', 3, 1, 1, NOW(), NOW()),\n"
    sql_content += "(4, 2, '启用', '1', '#52c41a', 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(5, 2, '禁用', '0', '#ff4d4f', 2, 1, 1, NOW(), NOW()),\n"
    sql_content += "(6, 3, '系统用户', '0', '#1890ff', 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(7, 3, '普通用户', '1', '#52c41a', 2, 1, 1, NOW(), NOW()),\n"
    sql_content += "(8, 3, '测试用户', '2', '#faad14', 3, 1, 1, NOW(), NOW()),\n"
    sql_content += "(9, 4, '全部数据', '0', '#1890ff', 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(10, 4, '本部门数据', '1', '#52c41a', 2, 1, 1, NOW(), NOW()),\n"
    sql_content += "(11, 4, '本部门及下级', '2', '#faad14', 3, 1, 1, NOW(), NOW()),\n"
    sql_content += "(12, 4, '仅本人数据', '3', '#ff4d4f', 4, 1, 1, NOW(), NOW()),\n"
    sql_content += "(13, 4, '自定义数据', '4', '#722ed1', 5, 1, 1, NOW(), NOW()),\n"
    sql_content += "(14, 5, '菜单', '0', '#1890ff', 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(15, 5, '按钮', '1', '#52c41a', 2, 1, 1, NOW(), NOW()),\n"
    sql_content += "(16, 5, 'API', '2', '#faad14', 3, 1, 1, NOW(), NOW()),\n"
    sql_content += "(17, 5, '数据', '3', '#ff4d4f', 4, 1, 1, NOW(), NOW()),\n"
    sql_content += "(18, 5, '字段', '4', '#722ed1', 5, 1, 1, NOW(), NOW()),\n"
    sql_content += "(19, 6, '目录', '0', '#1890ff', 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(20, 6, '菜单', '1', '#52c41a', 2, 1, 1, NOW(), NOW()),\n"
    sql_content += "(21, 6, '按钮', '2', '#faad14', 3, 1, 1, NOW(), NOW());\n\n"
    
    sql_content += "-- ============================================\n"
    sql_content += "-- 2. 系统配置\n"
    sql_content += "-- ============================================\n\n"
    sql_content += "INSERT INTO `sys_config` (`id`, `config_key`, `config_value`, `config_type`, `group_name`, `description`, `is_system`, `sort`, `tenant_id`, `status`, `created_at`, `updated_at`) VALUES\n"
    sql_content += "(1, 'site_name', '企业级RBAC系统', 'string', '基本设置', '网站名称', 1, 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(2, 'site_description', '基于Python FastAPI构建的企业级权限管理系统', 'string', '基本设置', '网站描述', 1, 2, 1, 1, NOW(), NOW()),\n"
    sql_content += "(3, 'register_enabled', '1', 'bool', '用户设置', '是否开启用户注册', 0, 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(4, 'password_min_length', '6', 'int', '用户设置', '密码最小长度', 0, 2, 1, 1, NOW(), NOW()),\n"
    sql_content += "(5, 'session_timeout', '7200', 'int', '安全设置', '会话超时时间(秒)', 1, 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(6, 'login_max_attempts', '5', 'int', '安全设置', '最大登录失败次数', 0, 2, 1, 1, NOW(), NOW()),\n"
    sql_content += "(7, 'copyright', '© 2026 Enterprise RBAC System', 'string', '基本设置', '版权信息', 0, 3, 1, 1, NOW(), NOW());\n\n"
    
    sql_content += "-- ============================================\n"
    sql_content += "-- 3. 部门\n"
    sql_content += "-- ============================================\n\n"
    sql_content += "INSERT INTO `sys_dept` (`id`, `name`, `code`, `description`, `parent_id`, `level`, `sort`, `tenant_id`, `status`, `created_at`, `updated_at`) VALUES\n"
    sql_content += "(1, '总公司', 'HQ', '集团总公司', NULL, 1, 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(2, '技术部', 'TECH', '技术研发部门', 1, 2, 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(3, '市场部', 'MARKET', '市场营销部门', 1, 2, 2, 1, 1, NOW(), NOW()),\n"
    sql_content += "(4, '人事部', 'HR', '人力资源部门', 1, 2, 3, 1, 1, NOW(), NOW()),\n"
    sql_content += "(5, '财务部', 'FINANCE', '财务部门', 1, 2, 4, 1, 1, NOW(), NOW()),\n"
    sql_content += "(6, '前端组', 'FRONTEND', '前端开发组', 2, 3, 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(7, '后端组', 'BACKEND', '后端开发组', 2, 3, 2, 1, 1, NOW(), NOW()),\n"
    sql_content += "(8, '测试组', 'TEST', '质量测试组', 2, 3, 3, 1, 1, NOW(), NOW()),\n"
    sql_content += "(9, '销售组', 'SALES', '产品销售组', 3, 3, 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(10, '运营组', 'OPERATION', '市场运营组', 3, 3, 2, 1, 1, NOW(), NOW());\n\n"
    
    sql_content += "-- ============================================\n"
    sql_content += "-- 4. 菜单\n"
    sql_content += "-- ============================================\n\n"
    sql_content += "INSERT INTO `sys_menu` (`id`, `name`, `code`, `type`, `path`, `component`, `icon`, `parent_id`, `level`, `sort`, `is_cache`, `is_visible`, `tenant_id`, `status`, `created_at`, `updated_at`) VALUES\n"
    sql_content += "(1, '首页', 'dashboard', 0, '/dashboard', NULL, 'HomeOutlined', NULL, 1, 1, 1, 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(2, '系统管理', 'system', 0, '/system', NULL, 'SettingOutlined', NULL, 1, 2, 1, 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(3, '日志管理', 'log', 0, '/log', NULL, 'FileTextOutlined', NULL, 1, 3, 1, 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(4, '个人中心', 'personal', 0, '/personal', NULL, 'UserOutlined', NULL, 1, 4, 1, 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(5, '用户管理', 'user', 0, '/system/user', NULL, 'UserOutlined', 2, 2, 1, 1, 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(6, '角色管理', 'role', 0, '/system/role', NULL, 'TeamOutlined', 2, 2, 2, 1, 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(7, '菜单管理', 'menu', 0, '/system/menu', NULL, 'MenuOutlined', 2, 2, 3, 1, 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(8, '部门管理', 'department', 0, '/system/department', NULL, 'ApartmentOutlined', 2, 2, 4, 1, 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(9, '用户组管理', 'user-group', 0, '/system/user-group', NULL, 'UsergroupAddOutlined', 2, 2, 5, 1, 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(10, '系统字典', 'dict', 0, '/system/dict', NULL, 'BookOutlined', 2, 2, 6, 1, 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(11, '系统配置', 'config', 0, '/system/config', NULL, 'ControlOutlined', 2, 2, 7, 1, 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(12, '操作日志', 'operation-log', 0, '/log/operation', NULL, 'FileTextOutlined', 3, 2, 1, 1, 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(13, '审计日志', 'audit-log', 0, '/log/audit', NULL, 'AuditOutlined', 3, 2, 2, 1, 1, 1, 1, NOW(), NOW());\n\n"
    
    sql_content += "-- ============================================\n"
    sql_content += "-- 5. 权限\n"
    sql_content += "-- ============================================\n\n"
    sql_content += "INSERT INTO `sys_permission` (`id`, `name`, `code`, `type`, `resource_type`, `action`, `path`, `method`, `parent_id`, `level`, `sort`, `tenant_id`, `status`, `created_at`, `updated_at`) VALUES\n"
    sql_content += "(1, '用户查看', 'user:view', 2, 'user', 'view', '/api/v1/users', 'GET', NULL, 1, 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(2, '用户创建', 'user:create', 2, 'user', 'create', '/api/v1/users', 'POST', NULL, 1, 2, 1, 1, NOW(), NOW()),\n"
    sql_content += "(3, '用户更新', 'user:update', 2, 'user', 'update', '/api/v1/users/*', 'PUT', NULL, 1, 3, 1, 1, NOW(), NOW()),\n"
    sql_content += "(4, '用户删除', 'user:delete', 2, 'user', 'delete', '/api/v1/users/*', 'DELETE', NULL, 1, 4, 1, 1, NOW(), NOW()),\n"
    sql_content += "(5, '角色查看', 'role:view', 2, 'role', 'view', '/api/v1/roles', 'GET', NULL, 1, 5, 1, 1, NOW(), NOW()),\n"
    sql_content += "(6, '角色创建', 'role:create', 2, 'role', 'create', '/api/v1/roles', 'POST', NULL, 1, 6, 1, 1, NOW(), NOW()),\n"
    sql_content += "(7, '角色更新', 'role:update', 2, 'role', 'update', '/api/v1/roles/*', 'PUT', NULL, 1, 7, 1, 1, NOW(), NOW()),\n"
    sql_content += "(8, '角色删除', 'role:delete', 2, 'role', 'delete', '/api/v1/roles/*', 'DELETE', NULL, 1, 8, 1, 1, NOW(), NOW()),\n"
    sql_content += "(9, '菜单查看', 'menu:view', 2, 'menu', 'view', '/api/v1/menus', 'GET', NULL, 1, 9, 1, 1, NOW(), NOW()),\n"
    sql_content += "(10, '菜单创建', 'menu:create', 2, 'menu', 'create', '/api/v1/menus', 'POST', NULL, 1, 10, 1, 1, NOW(), NOW()),\n"
    sql_content += "(11, '菜单更新', 'menu:update', 2, 'menu', 'update', '/api/v1/menus/*', 'PUT', NULL, 1, 11, 1, 1, NOW(), NOW()),\n"
    sql_content += "(12, '菜单删除', 'menu:delete', 2, 'menu', 'delete', '/api/v1/menus/*', 'DELETE', NULL, 1, 12, 1, 1, NOW(), NOW()),\n"
    sql_content += "(13, '部门查看', 'department:view', 2, 'department', 'view', '/api/v1/departments', 'GET', NULL, 1, 13, 1, 1, NOW(), NOW()),\n"
    sql_content += "(14, '部门创建', 'department:create', 2, 'department', 'create', '/api/v1/departments', 'POST', NULL, 1, 14, 1, 1, NOW(), NOW()),\n"
    sql_content += "(15, '部门更新', 'department:update', 2, 'department', 'update', '/api/v1/departments/*', 'PUT', NULL, 1, 15, 1, 1, NOW(), NOW()),\n"
    sql_content += "(16, '部门删除', 'department:delete', 2, 'department', 'delete', '/api/v1/departments/*', 'DELETE', NULL, 1, 16, 1, 1, NOW(), NOW()),\n"
    sql_content += "(17, '用户组查看', 'user-group:view', 2, 'user-group', 'view', '/api/v1/user-groups', 'GET', NULL, 1, 17, 1, 1, NOW(), NOW()),\n"
    sql_content += "(18, '用户组创建', 'user-group:create', 2, 'user-group', 'create', '/api/v1/user-groups', 'POST', NULL, 1, 18, 1, 1, NOW(), NOW()),\n"
    sql_content += "(19, '用户组更新', 'user-group:update', 2, 'user-group', 'update', '/api/v1/user-groups/*', 'PUT', NULL, 1, 19, 1, 1, NOW(), NOW()),\n"
    sql_content += "(20, '用户组删除', 'user-group:delete', 2, 'user-group', 'delete', '/api/v1/user-groups/*', 'DELETE', NULL, 1, 20, 1, 1, NOW(), NOW()),\n"
    sql_content += "(21, '字典查看', 'dict:view', 2, 'dict', 'view', '/api/v1/system-dicts', 'GET', NULL, 1, 21, 1, 1, NOW(), NOW()),\n"
    sql_content += "(22, '字典创建', 'dict:create', 2, 'dict', 'create', '/api/v1/system-dicts', 'POST', NULL, 1, 22, 1, 1, NOW(), NOW()),\n"
    sql_content += "(23, '字典更新', 'dict:update', 2, 'dict', 'update', '/api/v1/system-dicts/*', 'PUT', NULL, 1, 23, 1, 1, NOW(), NOW()),\n"
    sql_content += "(24, '字典删除', 'dict:delete', 2, 'dict', 'delete', '/api/v1/system-dicts/*', 'DELETE', NULL, 1, 24, 1, 1, NOW(), NOW()),\n"
    sql_content += "(25, '配置查看', 'config:view', 2, 'config', 'view', '/api/v1/system-configs', 'GET', NULL, 1, 25, 1, 1, NOW(), NOW()),\n"
    sql_content += "(26, '配置创建', 'config:create', 2, 'config', 'create', '/api/v1/system-configs', 'POST', NULL, 1, 26, 1, 1, NOW(), NOW()),\n"
    sql_content += "(27, '配置更新', 'config:update', 2, 'config', 'update', '/api/v1/system-configs/*', 'PUT', NULL, 1, 27, 1, 1, NOW(), NOW()),\n"
    sql_content += "(28, '配置删除', 'config:delete', 2, 'config', 'delete', '/api/v1/system-configs/*', 'DELETE', NULL, 1, 28, 1, 1, NOW(), NOW()),\n"
    sql_content += "(29, '操作日志查看', 'operation-log:view', 2, 'operation-log', 'view', '/api/v1/operation-logs', 'GET', NULL, 1, 29, 1, 1, NOW(), NOW()),\n"
    sql_content += "(30, '审计日志查看', 'audit-log:view', 2, 'audit-log', 'view', '/api/v1/audit-logs', 'GET', NULL, 1, 30, 1, 1, NOW(), NOW()),\n"
    sql_content += "(31, '权限查看', 'permission:view', 2, 'permission', 'view', '/api/v1/permissions', 'GET', NULL, 1, 31, 1, 1, NOW(), NOW());\n\n"
    
    sql_content += "-- ============================================\n"
    sql_content += "-- 6. 角色\n"
    sql_content += "-- ============================================\n\n"
    sql_content += "INSERT INTO `sys_role` (`id`, `name`, `code`, `type`, `data_scope`, `description`, `sort`, `tenant_id`, `status`, `created_at`, `updated_at`) VALUES\n"
    sql_content += "(1, '超级管理员', 'super_admin', 0, 0, '系统超级管理员，拥有所有权限', 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(2, '系统管理员', 'admin', 1, 0, '系统管理员，管理系统配置', 2, 1, 1, NOW(), NOW()),\n"
    sql_content += "(3, '部门经理', 'manager', 2, 2, '部门经理，管理本部门及下级数据', 3, 1, 1, NOW(), NOW()),\n"
    sql_content += "(4, '普通员工', 'staff', 3, 3, '普通员工，只能查看和编辑本人数据', 4, 1, 1, NOW(), NOW());\n\n"
    
    sql_content += "-- ============================================\n"
    sql_content += "-- 7. 用户组\n"
    sql_content += "-- ============================================\n\n"
    sql_content += "INSERT INTO `sys_user_group` (`id`, `name`, `code`, `description`, `sort`, `tenant_id`, `status`, `created_at`, `updated_at`) VALUES\n"
    sql_content += "(1, '技术团队', 'tech_team', '技术部全体成员', 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(2, '市场团队', 'market_team', '市场部全体成员', 2, 1, 1, NOW(), NOW()),\n"
    sql_content += "(3, '管理团队', 'management_team', '公司管理层', 3, 1, 1, NOW(), NOW()),\n"
    sql_content += "(4, '前端开发组', 'frontend_team', '前端开发团队', 4, 1, 1, NOW(), NOW()),\n"
    sql_content += "(5, '后端开发组', 'backend_team', '后端开发团队', 5, 1, 1, NOW(), NOW());\n\n"
    
    sql_content += "-- ============================================\n"
    sql_content += "-- 8. 用户 (密码: admin123 或 123456)\n"
    sql_content += "-- ============================================\n\n"
    sql_content += "INSERT INTO `sys_user` (`id`, `username`, `password`, `nickname`, `email`, `phone`, `avatar`, `department_id`, `tenant_id`, `status`, `created_at`, `updated_at`) VALUES\n"
    sql_content += "(1, 'admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/Lew5bKq5Kq5Kq5Kq', '系统管理员', 'admin@example.com', '13800138000', NULL, 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(2, 'zhangsan', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/Lew5bKq5Kq5Kq5Kq', '张三', 'zhangsan@example.com', '13800138001', NULL, 2, 1, 1, NOW(), NOW()),\n"
    sql_content += "(3, 'lisi', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/Lew5bKq5Kq5Kq5Kq', '李四', 'lisi@example.com', '13800138002', NULL, 3, 1, 1, NOW(), NOW()),\n"
    sql_content += "(4, 'wangwu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/Lew5bKq5Kq5Kq5Kq', '王五', 'wangwu@example.com', '13800138003', NULL, 6, 1, 1, NOW(), NOW()),\n"
    sql_content += "(5, 'zhaoliu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/Lew5bKq5Kq5Kq5Kq', '赵六', 'zhaoliu@example.com', '13800138004', NULL, 7, 1, 1, NOW(), NOW()),\n"
    sql_content += "(6, 'qianqi', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/Lew5bKq5Kq5Kq5Kq', '钱七', 'qianqi@example.com', '13800138005', NULL, 3, 1, 1, NOW(), NOW());\n\n"
    
    sql_content += "-- ============================================\n"
    sql_content += "-- 9. 用户档案\n"
    sql_content += "-- ============================================\n\n"
    sql_content += "INSERT INTO `sys_user_profile` (`id`, `user_id`, `gender`, `birthday`, `address`, `bio`, `tenant_id`, `created_at`, `updated_at`) VALUES\n"
    sql_content += "(1, 1, '1', NULL, NULL, NULL, 1, NOW(), NOW()),\n"
    sql_content += "(2, 2, '1', NULL, NULL, NULL, 1, NOW(), NOW()),\n"
    sql_content += "(3, 3, '2', NULL, NULL, NULL, 1, NOW(), NOW()),\n"
    sql_content += "(4, 4, '1', NULL, NULL, NULL, 1, NOW(), NOW()),\n"
    sql_content += "(5, 5, '1', NULL, NULL, NULL, 1, NOW(), NOW()),\n"
    sql_content += "(6, 6, '2', NULL, NULL, NULL, 1, NOW(), NOW());\n\n"
    
    sql_content += "-- ============================================\n"
    sql_content += "-- 10. 用户-角色关联\n"
    sql_content += "-- ============================================\n\n"
    sql_content += "INSERT INTO `sys_user_role` (`id`, `user_id`, `role_id`, `is_primary`, `tenant_id`, `created_at`, `updated_at`) VALUES\n"
    sql_content += "(1, 1, 1, 1, 1, NOW(), NOW()),\n"
    sql_content += "(2, 2, 2, 1, 1, NOW(), NOW()),\n"
    sql_content += "(3, 3, 3, 1, 1, NOW(), NOW()),\n"
    sql_content += "(4, 4, 4, 1, 1, NOW(), NOW()),\n"
    sql_content += "(5, 5, 4, 1, 1, NOW(), NOW()),\n"
    sql_content += "(6, 6, 4, 1, 1, NOW(), NOW());\n\n"
    
    sql_content += "-- ============================================\n"
    sql_content += "-- 11. 角色-权限关联 (超级管理员拥有所有权限)\n"
    sql_content += "-- ============================================\n\n"
    role_perm_values = []
    for i in range(1, 4):
        for perm_id in range(1, 32):
            role_perm_values.append(f"({(i-1)*31 + perm_id}, {i}, {perm_id}, 1, NOW(), NOW())")
    
    sql_content += "INSERT INTO `sys_role_permission` (`id`, `role_id`, `permission_id`, `tenant_id`, `created_at`, `updated_at`) VALUES\n"
    sql_content += ",\n".join(role_perm_values)
    sql_content += ";\n\n"
    
    sql_content += "-- ============================================\n"
    sql_content += "-- 12. 用户-用户组关联\n"
    sql_content += "-- ============================================\n\n"
    sql_content += "INSERT INTO `sys_user_group_relation` (`id`, `user_id`, `user_group_id`, `tenant_id`, `created_at`, `updated_at`) VALUES\n"
    sql_content += "(1, 1, 3, 1, NOW(), NOW()),\n"
    sql_content += "(2, 2, 1, 1, NOW(), NOW()),\n"
    sql_content += "(3, 2, 5, 1, NOW(), NOW()),\n"
    sql_content += "(4, 3, 2, 1, NOW(), NOW()),\n"
    sql_content += "(5, 4, 1, 1, NOW(), NOW()),\n"
    sql_content += "(6, 4, 4, 1, NOW(), NOW()),\n"
    sql_content += "(7, 5, 1, 1, NOW(), NOW()),\n"
    sql_content += "(8, 5, 5, 1, NOW(), NOW()),\n"
    sql_content += "(9, 6, 2, 1, NOW(), NOW());\n\n"
    
    sql_content += "-- ============================================\n"
    sql_content += "-- 13. 用户组-角色关联\n"
    sql_content += "-- ============================================\n\n"
    sql_content += "INSERT INTO `sys_user_group_role_relation` (`id`, `user_group_id`, `role_id`, `tenant_id`, `created_at`, `updated_at`) VALUES\n"
    sql_content += "(1, 1, 2, 1, NOW(), NOW()),\n"
    sql_content += "(2, 2, 3, 1, NOW(), NOW()),\n"
    sql_content += "(3, 3, 1, 1, NOW(), NOW()),\n"
    sql_content += "(4, 4, 4, 1, NOW(), NOW()),\n"
    sql_content += "(5, 5, 4, 1, NOW(), NOW());\n\n"
    
    sql_content += "SET FOREIGN_KEY_CHECKS = 1;\n"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(sql_content)
    
    print(f"[OK] 演示数据SQL已生成: {output_file}")


def main():
    print("=" * 70)
    print("企业RBAC系统 - SQL迁移文件生成器")
    print("=" * 70)
    
    migrations_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'migrations')
    if not os.path.exists(migrations_dir):
        os.makedirs(migrations_dir)
    
    schema_file = os.path.join(migrations_dir, '001_initial_schema.sql')
    data_file = os.path.join(migrations_dir, '002_demo_data.sql')
    
    generate_schema_sql(schema_file)
    generate_demo_data_sql(data_file)
    
    print("\n" + "=" * 70)
    print("[OK] SQL迁移文件生成成功！")
    print("=" * 70)


if __name__ == "__main__":
    main()
