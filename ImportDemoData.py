"""导入演示数据到数据库"""

import sys
import os
from datetime import datetime, timedelta
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from App.Config.Database import engine
from sqlalchemy import text
from App.Utils.Security import SecurityUtils

def import_demo_data():
    """导入演示数据"""
    with engine.connect() as conn:
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")
        
        print("开始导入演示数据...")
        
        # 1. 系统字典数据
        print("  1. 导入系统字典数据...")
        import_system_dict(conn)
        
        # 2. 系统配置数据
        print("  2. 导入系统配置数据...")
        import_system_config(conn)
        
        # 3. 部门数据
        print("  3. 导入部门数据...")
        import_departments(conn)
        
        # 4. 用户数据
        print("  4. 导入用户数据...")
        import_users(conn)
        
        # 5. 用户扩展信息数据
        print("  5. 导入用户扩展信息数据...")
        import_user_profiles(conn)
        
        # 6. 角色数据
        print("  6. 导入角色数据...")
        import_roles(conn)
        
        # 7. 权限数据
        print("  7. 导入权限数据...")
        import_permissions(conn)
        
        # 8. 菜单数据
        print("  8. 导入菜单数据...")
        import_menus(conn)
        
        # 9. 用户角色关联数据
        print("  9. 导入用户角色关联数据...")
        import_user_roles(conn)
        
        # 10. 角色权限关联数据
        print("  10. 导入角色权限关联数据...")
        import_role_permissions(conn)
        
        # 11. 菜单权限关联数据
        print("  11. 导入菜单权限关联数据...")
        import_menu_permissions(conn)
        
        # 12. 用户组数据
        print("  12. 导入用户组数据...")
        import_user_groups(conn)
        
        # 13. 用户组用户关联数据
        print("  13. 导入用户组用户关联数据...")
        import_user_group_users(conn)
        
        # 14. 用户组角色关联数据
        print("  14. 导入用户组角色关联数据...")
        import_user_group_roles(conn)
        
        # 15. 数据权限规则数据
        print("  15. 导入数据权限规则数据...")
        import_data_permission_rules(conn)
        
        # 16. 操作日志数据
        print("  16. 导入操作日志数据...")
        import_operation_logs(conn)
        
        # 17. 审计日志数据
        print("  17. 导入审计日志数据...")
        import_audit_logs(conn)
        
        # 18. 用户会话数据
        print("  18. 导入用户会话数据...")
        import_user_sessions(conn)
        
        print("演示数据导入完成！")

def import_system_dict(conn):
    """导入系统字典数据"""
    dicts = [
        ("性别", "gender", "用户性别字典", 1, 1),
        ("用户状态", "user_status", "用户状态字典", 1, 2),
        ("角色状态", "role_status", "角色状态字典", 1, 3),
        ("数据范围", "data_scope", "数据范围字典", 1, 4),
        ("操作状态", "operation_status", "操作状态字典", 1, 5)
    ]
    
    for dict_data in dicts:
        conn.execute(text("""
            INSERT INTO sys_dict (name, code, description, status, sort, create_time, update_time, is_deleted, version)
            VALUES (:name, :code, :description, :status, :sort, NOW(), NOW(), 0, 1)
        """), {
            'name': dict_data[0],
            'code': dict_data[1],
            'description': dict_data[2],
            'status': dict_data[3],
            'sort': dict_data[4]
        })
    
    # 获取刚插入的字典ID
    result = conn.execute(text("SELECT id, code FROM sys_dict"))
    dict_ids = {row[1]: row[0] for row in result}
    
    # 字典项数据
    dict_items = [
        ("gender", "未知", "0", "", "未知性别", 1, 1),
        ("gender", "男", "1", "blue", "男性", 1, 2),
        ("gender", "女", "2", "pink", "女性", 1, 3),
        ("user_status", "禁用", "0", "red", "用户已禁用", 1, 1),
        ("user_status", "启用", "1", "green", "用户已启用", 1, 2),
        ("role_status", "禁用", "0", "red", "角色已禁用", 1, 1),
        ("role_status", "启用", "1", "green", "角色已启用", 1, 2),
        ("data_scope", "全部", "0", "", "全部数据", 1, 1),
        ("data_scope", "本部门", "1", "", "本部门数据", 1, 2),
        ("data_scope", "本部门及下级", "2", "", "本部门及下级数据", 1, 3),
        ("data_scope", "仅本人", "3", "", "仅本人数据", 1, 4),
        ("data_scope", "自定义", "4", "", "自定义数据", 1, 5),
        ("operation_status", "失败", "0", "red", "操作失败", 1, 1),
        ("operation_status", "成功", "1", "green", "操作成功", 1, 2)
    ]
    
    for item in dict_items:
        dict_id = dict_ids.get(item[0])
        if dict_id:
            conn.execute(text("""
                INSERT INTO sys_dict_item (dict_id, label, value, color, description, status, sort, create_time, update_time, is_deleted, version)
                VALUES (:dict_id, :label, :value, :color, :description, :status, :sort, NOW(), NOW(), 0, 1)
            """), {
                'dict_id': dict_id,
                'label': item[1],
                'value': item[2],
                'color': item[3],
                'description': item[4],
                'status': item[5],
                'sort': item[6]
            })

def import_system_config(conn):
    """导入系统配置数据"""
    configs = [
        ("site_name", "企业RBAC系统", "string", "网站名称", "system", 1, 1, 1),
        ("site_logo", "", "string", "网站Logo", "system", 1, 1, 2),
        ("site_description", "企业级RBAC权限管理系统", "string", "网站描述", "system", 1, 1, 3),
        ("user_default_password", "123456", "string", "用户默认密码", "system", 1, 1, 4),
        ("session_expire_minutes", "30", "int", "会话过期时间(分钟)", "system", 1, 1, 5),
        ("max_login_attempts", "5", "int", "最大登录尝试次数", "system", 1, 1, 6),
        ("enable_captcha", "false", "bool", "是否启用验证码", "security", 1, 1, 7),
        ("upload_max_size", "5242880", "int", "上传文件最大大小(字节)", "system", 1, 1, 8)
    ]
    
    for config in configs:
        conn.execute(text("""
            INSERT INTO sys_config (config_key, config_value, config_type, description, group_name, is_system, status, sort, create_time, update_time, is_deleted, version)
            VALUES (:config_key, :config_value, :config_type, :description, :group_name, :is_system, :status, :sort, NOW(), NOW(), 0, 1)
        """), {
            'config_key': config[0],
            'config_value': config[1],
            'config_type': config[2],
            'description': config[3],
            'group_name': config[4],
            'is_system': config[5],
            'status': config[6],
            'sort': config[7]
        })

def import_departments(conn):
    """导入部门数据"""
    departments = [
        (1, "总公司", "head_office", None, 1, "010-88888888", "北京市朝阳区建国路88号", "总公司", 1),
        (1, "技术部", "tech_department", 1, 2, "010-88888801", "北京市朝阳区建国路88号3层", "技术研发部门", 1),
        (1, "产品部", "product_department", 1, 2, "010-88888802", "北京市朝阳区建国路88号5层", "产品管理部门", 1),
        (1, "市场部", "market_department", 1, 2, "010-88888803", "北京市朝阳区建国路88号6层", "市场营销部门", 1),
        (1, "人事部", "hr_department", 1, 2, "010-88888804", "北京市朝阳区建国路88号8层", "人力资源部门", 1),
        (1, "前端组", "frontend_team", 2, 3, "010-88888811", "北京市朝阳区建国路88号3层301室", "前端开发小组", 1),
        (1, "后端组", "backend_team", 2, 3, "010-88888812", "北京市朝阳区建国路88号3层302室", "后端开发小组", 1),
        (1, "测试组", "test_team", 2, 3, "010-88888813", "北京市朝阳区建国路88号3层303室", "测试小组", 1)
    ]
    
    for dept in departments:
        conn.execute(text("""
            INSERT INTO sys_department (tenant_id, name, code, parent_id, leader_id, level, contact_phone, address, description, status, create_time, update_time, is_deleted, version)
            VALUES (:tenant_id, :name, :code, :parent_id, :leader_id, :level, :contact_phone, :address, :description, :status, NOW(), NOW(), 0, 1)
        """), {
            'tenant_id': dept[0],
            'name': dept[1],
            'code': dept[2],
            'parent_id': dept[3],
            'leader_id': None,
            'level': dept[4],
            'contact_phone': dept[5],
            'address': dept[6],
            'description': dept[7],
            'status': dept[8]
        })

def import_users(conn):
    """导入用户数据"""
    password_hash = "$2b$12$EixZaY6sZ5j1Z5j1Z5j1Ze6sZ5j1Z5j1Z5j1Z5j1Z5j1Z5j1Z5j1Z5"
    
    users = [
        (1, "admin", password_hash, "系统管理员", "admin@example.com", "13800138000", None, 2, 1, None, None),
        (1, "zhangsan", password_hash, "张三", "zhangsan@example.com", "13800138001", None, 6, 1, None, None),
        (1, "lisi", password_hash, "李四", "lisi@example.com", "13800138002", None, 6, 1, None, None),
        (1, "wangwu", password_hash, "王五", "wangwu@example.com", "13800138003", None, 7, 1, None, None),
        (1, "zhaoliu", password_hash, "赵六", "zhaoliu@example.com", "13800138004", None, 7, 1, None, None),
        (1, "sunqi", password_hash, "孙七", "sunqi@example.com", "13800138005", None, 8, 1, None, None),
        (1, "zhouba", password_hash, "周八", "zhouba@example.com", "13800138006", None, 3, 1, None, None),
        (1, "wujiu", password_hash, "吴九", "wujiu@example.com", "13800138007", None, 4, 1, None, None),
        (1, "zhengshi", password_hash, "郑十", "zhengshi@example.com", "13800138008", None, 5, 1, None, None)
    ]
    
    for user in users:
        conn.execute(text("""
            INSERT INTO sys_user (tenant_id, username, password, nickname, email, phone, avatar, department_id, status, last_login_time, last_login_ip, create_time, update_time, is_deleted, version)
            VALUES (:tenant_id, :username, :password, :nickname, :email, :phone, :avatar, :department_id, :status, :last_login_time, :last_login_ip, NOW(), NOW(), 0, 1)
        """), {
            'tenant_id': user[0],
            'username': user[1],
            'password': user[2],
            'nickname': user[3],
            'email': user[4],
            'phone': user[5],
            'avatar': user[6],
            'department_id': user[7],
            'status': user[8],
            'last_login_time': user[9],
            'last_login_ip': user[10]
        })

def import_user_profiles(conn):
    """导入用户扩展信息数据"""
    # 获取用户ID
    result = conn.execute(text("SELECT id, username FROM sys_user"))
    users = {row[1]: row[0] for row in result}
    
    profiles = [
        ("admin", 1, None, None, "北京市朝阳区", "张总", "13900139000", "CEO", "2020-01-01", "系统管理员"),
        ("zhangsan", 1, "1990-01-15", "110101199001151234", "北京市海淀区", "张三妈妈", "13900139001", "前端工程师", "2021-03-15", "负责前端开发"),
        ("lisi", 1, "1991-05-20", "110101199105201234", "北京市西城区", "李四爸爸", "13900139002", "前端架构师", "2020-08-10", "负责前端架构"),
        ("wangwu", 2, "1989-08-10", "110101198908101234", "北京市东城区", "王五妻子", "13900139003", "后端工程师", "2019-11-20", "负责后端开发"),
        ("zhaoliu", 1, "1992-03-25", "110101199203251234", "北京市丰台区", "赵六父亲", "13900139004", "后端架构师", "2018-06-05", "负责后端架构"),
        ("sunqi", 2, "1993-11-08", "110101199311081234", "北京市石景山区", "孙七丈夫", "13900139005", "测试工程师", "2022-01-10", "负责测试工作"),
        ("zhouba", 1, "1988-07-12", "110101198807121234", "北京市通州区", "周八姐姐", "13900139006", "产品经理", "2017-09-15", "负责产品设计"),
        ("wujiu", 2, "1995-02-28", "110101199502281234", "北京市顺义区", "吴九弟弟", "13900139007", "市场专员", "2023-02-20", "负责市场推广"),
        ("zhengshi", 1, "1994-09-18", "110101199409181234", "北京市昌平区", "郑十哥哥", "13900139008", "人事专员", "2021-07-01", "负责人事管理")
    ]
    
    for profile in profiles:
        user_id = users.get(profile[0])
        if user_id:
            conn.execute(text("""
                INSERT INTO sys_user_profile (tenant_id, user_id, gender, birthday, id_card, address, emergency_contact, emergency_phone, position, entry_date, remark, create_time, update_time, is_deleted, version)
                VALUES (:tenant_id, :user_id, :gender, :birthday, :id_card, :address, :emergency_contact, :emergency_phone, :position, :entry_date, :remark, NOW(), NOW(), 0, 1)
            """), {
                'tenant_id': 1,
                'user_id': user_id,
                'gender': profile[1],
                'birthday': profile[2],
                'id_card': profile[3],
                'address': profile[4],
                'emergency_contact': profile[5],
                'emergency_phone': profile[6],
                'position': profile[7],
                'entry_date': profile[8],
                'remark': profile[9]
            })

def import_roles(conn):
    """导入角色数据"""
    roles = [
        (1, "超级管理员", "super_admin", None, 1, 0, 0, 1, "系统最高权限角色", 1),
        (1, "系统管理员", "system_admin", 1, 2, 0, 1, 2, "系统管理角色", 1),
        (1, "部门经理", "dept_manager", None, 1, 3, 2, 3, "部门管理角色", 1),
        (1, "普通员工", "normal_user", None, 1, 3, 3, 4, "普通员工角色", 1),
        (1, "前端开发", "frontend_dev", None, 1, 3, 4, 5, "前端开发角色", 1),
        (1, "后端开发", "backend_dev", None, 1, 3, 5, 6, "后端开发角色", 1),
        (1, "测试工程师", "test_engineer", None, 1, 3, 6, 7, "测试角色", 1),
        (1, "产品经理", "product_manager", None, 1, 3, 7, 8, "产品经理角色", 1)
    ]
    
    for role in roles:
        conn.execute(text("""
            INSERT INTO sys_role (tenant_id, name, code, parent_id, level, type, data_scope, sort, description, status, create_time, update_time, is_deleted, version)
            VALUES (:tenant_id, :name, :code, :parent_id, :level, :type, :data_scope, :sort, :description, :status, NOW(), NOW(), 0, 1)
        """), {
            'tenant_id': role[0],
            'name': role[1],
            'code': role[2],
            'parent_id': role[3],
            'level': role[4],
            'type': role[5],
            'data_scope': role[6],
            'sort': role[7],
            'description': role[8],
            'status': role[9]
        })

def import_permissions(conn):
    """导入权限数据"""
    permissions = [
        (1, "用户管理", "user_manage", None, 1, 0, "menu", None, "view", "/users", "GET", None, 1, 1),
        (1, "用户列表", "user_list", 1, 2, 1, "menu", None, "view", "/api/v1/users", "GET", None, 1, 1),
        (1, "创建用户", "user_create", 1, 2, 1, "button", None, "create", "/api/v1/users", "POST", None, 1, 2),
        (1, "编辑用户", "user_edit", 1, 2, 1, "button", None, "update", "/api/v1/users/:id", "PUT", None, 1, 3),
        (1, "删除用户", "user_delete", 1, 2, 1, "button", None, "delete", "/api/v1/users/:id", "DELETE", None, 1, 4),
        (1, "角色管理", "role_manage", None, 1, 0, "menu", None, "view", "/roles", "GET", None, 1, 2),
        (1, "角色列表", "role_list", 6, 2, 1, "menu", None, "view", "/api/v1/roles", "GET", None, 1, 1),
        (1, "创建角色", "role_create", 6, 2, 1, "button", None, "create", "/api/v1/roles", "POST", None, 1, 2),
        (1, "编辑角色", "role_edit", 6, 2, 1, "button", None, "update", "/api/v1/roles/:id", "PUT", None, 1, 3),
        (1, "删除角色", "role_delete", 6, 2, 1, "button", None, "delete", "/api/v1/roles/:id", "DELETE", None, 1, 4),
        (1, "权限管理", "permission_manage", None, 1, 0, "menu", None, "view", "/permissions", "GET", None, 1, 3),
        (1, "权限列表", "permission_list", 11, 2, 1, "menu", None, "view", "/api/v1/permissions", "GET", None, 1, 1),
        (1, "部门管理", "dept_manage", None, 1, 0, "menu", None, "view", "/departments", "GET", None, 1, 4),
        (1, "部门列表", "dept_list", 14, 2, 1, "menu", None, "view", "/api/v1/departments", "GET", None, 1, 1),
        (1, "创建部门", "dept_create", 14, 2, 1, "button", None, "create", "/api/v1/departments", "POST", None, 1, 2),
        (1, "编辑部门", "dept_edit", 14, 2, 1, "button", None, "update", "/api/v1/departments/:id", "PUT", None, 1, 3),
        (1, "删除部门", "dept_delete", 14, 2, 1, "button", None, "delete", "/api/v1/departments/:id", "DELETE", None, 1, 4),
        (1, "菜单管理", "menu_manage", None, 1, 0, "menu", None, "view", "/menus", "GET", None, 1, 5),
        (1, "菜单列表", "menu_list", 19, 2, 1, "menu", None, "view", "/api/v1/menus", "GET", None, 1, 1),
        (1, "创建菜单", "menu_create", 19, 2, 1, "button", None, "create", "/api/v1/menus", "POST", None, 1, 2),
        (1, "编辑菜单", "menu_edit", 19, 2, 1, "button", None, "update", "/api/v1/menus/:id", "PUT", None, 1, 3),
        (1, "删除菜单", "menu_delete", 19, 2, 1, "button", None, "delete", "/api/v1/menus/:id", "DELETE", None, 1, 4),
        (1, "系统设置", "system_setting", None, 1, 0, "menu", None, "view", "/settings", "GET", None, 1, 6),
        (1, "系统配置", "system_config", 25, 2, 1, "menu", None, "view", "/api/v1/config", "GET", None, 1, 1),
        (1, "字典管理", "dict_manage", 25, 2, 1, "menu", None, "view", "/api/v1/dicts", "GET", None, 1, 2),
        (1, "操作日志", "operation_log", None, 1, 0, "menu", None, "view", "/operation-logs", "GET", None, 1, 7),
        (1, "日志列表", "log_list", 29, 2, 1, "menu", None, "view", "/api/v1/operation-logs", "GET", None, 1, 1)
    ]
    
    for perm in permissions:
        conn.execute(text("""
            INSERT INTO sys_permission (tenant_id, name, code, parent_id, level, type, resource_type, resource_id, action, path, method, status, description, create_time, update_time, is_deleted, version)
            VALUES (:tenant_id, :name, :code, :parent_id, :level, :type, :resource_type, :resource_id, :action, :path, :method, :status, :description, NOW(), NOW(), 0, 1)
        """), {
            'tenant_id': perm[0],
            'name': perm[1],
            'code': perm[2],
            'parent_id': perm[3],
            'level': perm[4],
            'type': perm[5],
            'resource_type': perm[6],
            'resource_id': perm[7],
            'action': perm[8],
            'path': perm[9],
            'method': perm[10],
            'status': perm[11],
            'description': perm[12]
        })

def import_menus(conn):
    """导入菜单数据"""
    menus = [
        (1, "仪表盘", "dashboard", None, 1, 1, "/dashboard", "Dashboard", "HomeOutlined", 1, 1),
        (1, "系统管理", "system_manage", None, 1, 0, "/system", "Layout", "SettingOutlined", 2, 1),
        (1, "用户管理", "user_manage", 2, 2, 1, "/system/users", "UserList", "UserOutlined", 1, 1),
        (1, "角色管理", "role_manage", 2, 2, 1, "/system/roles", "RoleList", "TeamOutlined", 2, 1),
        (1, "权限管理", "permission_manage", 2, 2, 1, "/system/permissions", "PermissionList", "KeyOutlined", 3, 1),
        (1, "部门管理", "dept_manage", 2, 2, 1, "/system/departments", "DepartmentList", "ApartmentOutlined", 4, 1),
        (1, "菜单管理", "menu_manage", 2, 2, 1, "/system/menus", "MenuList", "MenuOutlined", 5, 1),
        (1, "系统设置", "system_setting", 2, 2, 0, "/system/settings", "Layout", "ToolOutlined", 6, 1),
        (1, "系统配置", "system_config", 8, 3, 1, "/system/settings/config", "SystemConfig", "SettingOutlined", 1, 1),
        (1, "字典管理", "dict_manage", 8, 3, 1, "/system/settings/dict", "DictList", "BookOutlined", 2, 1),
        (1, "日志管理", "log_manage", 2, 2, 0, "/system/logs", "Layout", "FileTextOutlined", 7, 1),
        (1, "操作日志", "operation_log", 11, 3, 1, "/system/logs/operation", "OperationLog", "HistoryOutlined", 1, 1),
        (1, "审计日志", "audit_log", 11, 3, 1, "/system/logs/audit", "AuditLog", "AuditOutlined", 2, 1)
    ]
    
    for menu in menus:
        conn.execute(text("""
            INSERT INTO sys_menu (tenant_id, name, code, parent_id, level, type, path, component, icon, sort, status, create_time, update_time, is_deleted, version)
            VALUES (:tenant_id, :name, :code, :parent_id, :level, :type, :path, :component, :icon, :sort, :status, NOW(), NOW(), 0, 1)
        """), {
            'tenant_id': menu[0],
            'name': menu[1],
            'code': menu[2],
            'parent_id': menu[3],
            'level': menu[4],
            'type': menu[5],
            'path': menu[6],
            'component': menu[7],
            'icon': menu[8],
            'sort': menu[9],
            'status': menu[10]
        })

def import_user_roles(conn):
    """导入用户角色关联数据"""
    result = conn.execute(text("SELECT id, username FROM sys_user"))
    users = {row[1]: row[0] for row in result}
    
    result = conn.execute(text("SELECT id, code FROM sys_role"))
    roles = {row[1]: row[0] for row in result}
    
    user_roles = [
        ("admin", "super_admin", True, None, None, 1),
        ("zhangsan", "frontend_dev", False, None, None, 1),
        ("lisi", "frontend_dev", False, None, None, 1),
        ("wangwu", "backend_dev", False, None, None, 1),
        ("zhaoliu", "backend_dev", False, None, None, 1),
        ("sunqi", "test_engineer", False, None, None, 1),
        ("zhouba", "product_manager", False, None, None, 1),
        ("wujiu", "normal_user", False, None, None, 1),
        ("zhengshi", "normal_user", False, None, None, 1)
    ]
    
    for ur in user_roles:
        user_id = users.get(ur[0])
        role_id = roles.get(ur[1])
        if user_id and role_id:
            conn.execute(text("""
                INSERT INTO sys_user_role (tenant_id, user_id, role_id, is_primary, effective_time, expire_time, status, create_time, update_time, is_deleted, version)
                VALUES (:tenant_id, :user_id, :role_id, :is_primary, :effective_time, :expire_time, :status, NOW(), NOW(), 0, 1)
            """), {
                'tenant_id': 1,
                'user_id': user_id,
                'role_id': role_id,
                'is_primary': ur[2],
                'effective_time': ur[3],
                'expire_time': ur[4],
                'status': ur[5]
            })

def import_role_permissions(conn):
    """导入角色权限关联数据"""
    result = conn.execute(text("SELECT id, code FROM sys_role"))
    roles = {row[1]: row[0] for row in result}
    
    result = conn.execute(text("SELECT id, code FROM sys_permission"))
    permissions = {row[1]: row[0] for row in result}
    
    # 超级管理员拥有所有权限
    super_admin_role_id = roles.get("super_admin")
    if super_admin_role_id:
        for perm_code, perm_id in permissions.items():
            conn.execute(text("""
                INSERT INTO sys_role_permission (tenant_id, role_id, permission_id, status, create_time, update_time, is_deleted, version)
                VALUES (:tenant_id, :role_id, :permission_id, :status, NOW(), NOW(), 0, 1)
            """), {
                'tenant_id': 1,
                'role_id': super_admin_role_id,
                'permission_id': perm_id,
                'status': 1
            })
    
    # 其他角色分配部分权限
    role_perms = [
        ("system_admin", ["user_manage", "user_list", "user_create", "user_edit", "user_delete", 
                          "role_manage", "role_list", "role_create", "role_edit", "role_delete",
                          "dept_manage", "dept_list", "dept_create", "dept_edit", "dept_delete",
                          "menu_manage", "menu_list", "menu_create", "menu_edit", "menu_delete",
                          "system_setting", "system_config", "dict_manage",
                          "operation_log", "log_list"]),
        ("dept_manager", ["user_manage", "user_list", "dept_manage", "dept_list"]),
        ("normal_user", ["user_list"]),
        ("frontend_dev", ["user_list", "dept_list"]),
        ("backend_dev", ["user_list", "dept_list"]),
        ("test_engineer", ["user_list", "dept_list"]),
        ("product_manager", ["user_list", "dept_list"])
    ]
    
    for rp in role_perms:
        role_id = roles.get(rp[0])
        if role_id:
            for perm_code in rp[1]:
                perm_id = permissions.get(perm_code)
                if perm_id:
                    conn.execute(text("""
                        INSERT INTO sys_role_permission (tenant_id, role_id, permission_id, status, create_time, update_time, is_deleted, version)
                        VALUES (:tenant_id, :role_id, :permission_id, :status, NOW(), NOW(), 0, 1)
                    """), {
                        'tenant_id': 1,
                        'role_id': role_id,
                        'permission_id': perm_id,
                        'status': 1
                    })

def import_menu_permissions(conn):
    """导入菜单权限关联数据"""
    result = conn.execute(text("SELECT id, code FROM sys_menu"))
    menus = {row[1]: row[0] for row in result}
    
    result = conn.execute(text("SELECT id, code FROM sys_permission"))
    permissions = {row[1]: row[0] for row in result}
    
    menu_perms = [
        ("user_manage", "user_manage"),
        ("user_manage", "user_list"),
        ("user_manage", "user_create"),
        ("user_manage", "user_edit"),
        ("user_manage", "user_delete"),
        ("role_manage", "role_manage"),
        ("role_manage", "role_list"),
        ("role_manage", "role_create"),
        ("role_manage", "role_edit"),
        ("role_manage", "role_delete"),
        ("dept_manage", "dept_manage"),
        ("dept_manage", "dept_list"),
        ("dept_manage", "dept_create"),
        ("dept_manage", "dept_edit"),
        ("dept_manage", "dept_delete"),
        ("menu_manage", "menu_manage"),
        ("menu_manage", "menu_list"),
        ("menu_manage", "menu_create"),
        ("menu_manage", "menu_edit"),
        ("menu_manage", "menu_delete"),
        ("system_config", "system_config"),
        ("dict_manage", "dict_manage"),
        ("operation_log", "operation_log"),
        ("operation_log", "log_list")
    ]
    
    for mp in menu_perms:
        menu_id = menus.get(mp[0])
        perm_id = permissions.get(mp[1])
        if menu_id and perm_id:
            conn.execute(text("""
                INSERT INTO sys_menu_permission (tenant_id, menu_id, permission_id, status, create_time, update_time, is_deleted, version)
                VALUES (:tenant_id, :menu_id, :permission_id, :status, NOW(), NOW(), 0, 1)
            """), {
                'tenant_id': 1,
                'menu_id': menu_id,
                'permission_id': perm_id,
                'status': 1
            })

def import_user_groups(conn):
    """导入用户组数据"""
    user_groups = [
        (1, "技术团队", "tech_team", "技术部门所有员工", 1, 1),
        (1, "产品团队", "product_team", "产品部门所有员工", 1, 2),
        (1, "市场团队", "market_team", "市场部门所有员工", 1, 3),
        (1, "开发团队", "dev_team", "所有开发人员", 1, 4)
    ]
    
    for ug in user_groups:
        conn.execute(text("""
            INSERT INTO sys_user_group (tenant_id, name, code, description, status, sort, create_time, update_time, is_deleted, version)
            VALUES (:tenant_id, :name, :code, :description, :status, :sort, NOW(), NOW(), 0, 1)
        """), {
            'tenant_id': ug[0],
            'name': ug[1],
            'code': ug[2],
            'description': ug[3],
            'status': ug[4],
            'sort': ug[5]
        })

def import_user_group_users(conn):
    """导入用户组用户关联数据"""
    result = conn.execute(text("SELECT id, username FROM sys_user"))
    users = {row[1]: row[0] for row in result}
    
    result = conn.execute(text("SELECT id, code FROM sys_user_group"))
    user_groups = {row[1]: row[0] for row in result}
    
    group_users = [
        ("tech_team", ["zhangsan", "lisi", "wangwu", "zhaoliu", "sunqi"]),
        ("product_team", ["zhouba"]),
        ("market_team", ["wujiu"]),
        ("dev_team", ["zhangsan", "lisi", "wangwu", "zhaoliu", "sunqi"])
    ]
    
    for gu in group_users:
        group_id = user_groups.get(gu[0])
        if group_id:
            for username in gu[1]:
                user_id = users.get(username)
                if user_id:
                    conn.execute(text("""
                        INSERT INTO sys_user_group_user (tenant_id, user_group_id, user_id, status, create_time, update_time, is_deleted, version)
                        VALUES (:tenant_id, :user_group_id, :user_id, :status, NOW(), NOW(), 0, 1)
                    """), {
                        'tenant_id': 1,
                        'user_group_id': group_id,
                        'user_id': user_id,
                        'status': 1
                    })

def import_user_group_roles(conn):
    """导入用户组角色关联数据"""
    result = conn.execute(text("SELECT id, code FROM sys_user_group"))
    user_groups = {row[1]: row[0] for row in result}
    
    result = conn.execute(text("SELECT id, code FROM sys_role"))
    roles = {row[1]: row[0] for row in result}
    
    group_roles = [
        ("tech_team", ["frontend_dev", "backend_dev", "test_engineer"]),
        ("product_team", ["product_manager"]),
        ("dev_team", ["frontend_dev", "backend_dev"])
    ]
    
    for gr in group_roles:
        group_id = user_groups.get(gr[0])
        if group_id:
            for role_code in gr[1]:
                role_id = roles.get(role_code)
                if role_id:
                    conn.execute(text("""
                        INSERT INTO sys_user_group_role (tenant_id, user_group_id, role_id, status, create_time, update_time, is_deleted, version)
                        VALUES (:tenant_id, :user_group_id, :role_id, :status, NOW(), NOW(), 0, 1)
                    """), {
                        'tenant_id': 1,
                        'user_group_id': group_id,
                        'role_id': role_id,
                        'status': 1
                    })

def import_data_permission_rules(conn):
    """导入数据权限规则数据"""
    result = conn.execute(text("SELECT id, code FROM sys_permission"))
    permissions = {row[1]: row[0] for row in result}
    
    rules = [
        (1, "查看全部用户", "view_all_users", "user_list", "sys_user", 0, None, 1, "查看全部用户数据"),
        (1, "查看本部门用户", "view_dept_users", "user_list", "sys_user", 1, None, 1, "查看本部门用户数据"),
        (1, "查看本人数据", "view_self_data", "user_list", "sys_user", 3, None, 1, "仅查看本人数据")
    ]
    
    for rule in rules:
        perm_id = permissions.get(rule[2])
        if perm_id:
            conn.execute(text("""
                INSERT INTO sys_data_permission_rule (tenant_id, name, code, permission_id, resource_table, rule_type, rule_expression, status, description, create_time, update_time, is_deleted, version)
                VALUES (:tenant_id, :name, :code, :permission_id, :resource_table, :rule_type, :rule_expression, :status, :description, NOW(), NOW(), 0, 1)
            """), {
                'tenant_id': rule[0],
                'name': rule[1],
                'code': rule[2],
                'permission_id': perm_id,
                'resource_table': rule[4],
                'rule_type': rule[5],
                'rule_expression': rule[6],
                'status': rule[7],
                'description': rule[8]
            })

def import_operation_logs(conn):
    """导入操作日志数据"""
    result = conn.execute(text("SELECT id, username FROM sys_user LIMIT 3"))
    users = list(result)
    
    modules = ["用户管理", "角色管理", "权限管理", "部门管理", "菜单管理", "系统设置"]
    operations = ["登录", "创建", "编辑", "删除", "查询", "导出"]
    
    for i in range(50):
        user = random.choice(users) if users else (None, None)
        module = random.choice(modules)
        operation = random.choice(operations)
        status = random.choice([0, 1])
        log_time = datetime.now() - timedelta(days=random.randint(0, 30))
        
        conn.execute(text("""
            INSERT INTO sys_operation_log (tenant_id, user_id, username, module, operation, description, request_method, request_url, request_params, response_result, execution_time, ip_address, user_agent, status, error_message, create_time, update_time, is_deleted, version)
            VALUES (:tenant_id, :user_id, :username, :module, :operation, :description, :request_method, :request_url, :request_params, :response_result, :execution_time, :ip_address, :user_agent, :status, :error_message, :create_time, :create_time, 0, 1)
        """), {
            'tenant_id': 1,
            'user_id': user[0] if user else None,
            'username': user[1] if user else None,
            'module': module,
            'operation': operation,
            'description': f"{operation}操作",
            'request_method': random.choice(["GET", "POST", "PUT", "DELETE"]),
            'request_url': f"/api/v1/{module.lower()}",
            'request_params': None,
            'response_result': None,
            'execution_time': random.randint(10, 500),
            'ip_address': f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}",
            'user_agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            'status': status,
            'error_message': "操作失败" if status == 0 else None,
            'create_time': log_time
        })

def import_audit_logs(conn):
    """导入审计日志数据"""
    result = conn.execute(text("SELECT id, username FROM sys_user LIMIT 3"))
    users = list(result)
    
    tables = ["sys_user", "sys_role", "sys_permission", "sys_department"]
    operations = ["INSERT", "UPDATE", "DELETE"]
    
    for i in range(30):
        user = random.choice(users) if users else (None, None)
        table = random.choice(tables)
        operation = random.choice(operations)
        log_time = datetime.now() - timedelta(days=random.randint(0, 30))
        
        conn.execute(text("""
            INSERT INTO sys_audit_log (tenant_id, table_name, record_id, operation_type, field_name, old_value, new_value, user_id, username, change_reason, create_time, update_time, is_deleted, version)
            VALUES (:tenant_id, :table_name, :record_id, :operation_type, :field_name, :old_value, :new_value, :user_id, :username, :change_reason, :create_time, :create_time, 0, 1)
        """), {
            'tenant_id': 1,
            'table_name': table,
            'record_id': random.randint(1, 10),
            'operation_type': operation,
            'field_name': "name" if operation == "UPDATE" else None,
            'old_value': "旧值" if operation == "UPDATE" else None,
            'new_value': "新值" if operation in ["INSERT", "UPDATE"] else None,
            'user_id': user[0] if user else None,
            'username': user[1] if user else None,
            'change_reason': "系统操作",
            'create_time': log_time
        })

def import_user_sessions(conn):
    """导入用户会话数据"""
    result = conn.execute(text("SELECT id, username FROM sys_user"))
    users = list(result)
    
    for user in users:
        for i in range(2):
            login_time = datetime.now() - timedelta(days=random.randint(0, 7))
            last_active_time = login_time + timedelta(minutes=random.randint(5, 120))
            expire_time = last_active_time + timedelta(minutes=30)
            
            conn.execute(text("""
                INSERT INTO sys_user_session (tenant_id, user_id, session_id, access_token, refresh_token, device_type, device_info, ip_address, login_time, last_active_time, expire_time, status, create_time, update_time, is_deleted, version)
                VALUES (:tenant_id, :user_id, :session_id, :access_token, :refresh_token, :device_type, :device_info, :ip_address, :login_time, :last_active_time, :expire_time, :status, NOW(), NOW(), 0, 1)
            """), {
                'tenant_id': 1,
                'user_id': user[0],
                'session_id': f"session_{user[0]}_{random.randint(1000, 9999)}",
                'access_token': f"access_token_{random.randint(1000, 9999)}",
                'refresh_token': f"refresh_token_{random.randint(1000, 9999)}",
                'device_type': random.choice(["web", "mobile", "desktop"]),
                'device_info': "Windows 10 / Chrome 120.0",
                'ip_address': f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}",
                'login_time': login_time,
                'last_active_time': last_active_time,
                'expire_time': expire_time,
                'status': 1 if expire_time > datetime.now() else 0
            })

if __name__ == "__main__":
    import_demo_data()
