-- =============================================================
-- 企业级RBAC系统 - 演示数据脚本
-- 版本: 1.0.0
-- 日期: 2026-04-13
-- 说明: 包含完整的演示数据，admin用户拥有所有权限
-- =============================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- =============================================================
-- 清空已有数据（按依赖关系倒序）
-- =============================================================
SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE `sys_operation_log`;
TRUNCATE TABLE `sys_audit_log`;
TRUNCATE TABLE `sys_user_session`;
TRUNCATE TABLE `sys_user_group_role_relation`;
TRUNCATE TABLE `sys_user_group_relation`;
TRUNCATE TABLE `sys_user_group`;
TRUNCATE TABLE `sys_user_profile`;
TRUNCATE TABLE `sys_user_role`;
TRUNCATE TABLE `sys_role_permission`;
TRUNCATE TABLE `sys_menu_permission`;
TRUNCATE TABLE `sys_permission`;
TRUNCATE TABLE `sys_menu`;
TRUNCATE TABLE `sys_role`;
TRUNCATE TABLE `sys_user`;
TRUNCATE TABLE `sys_dept`;
TRUNCATE TABLE `sys_dict_item`;
TRUNCATE TABLE `sys_dict`;
TRUNCATE TABLE `sys_config`;
TRUNCATE TABLE `sys_data_permission_rule`;

-- =============================================================
-- 1. 插入部门数据
-- =============================================================
INSERT INTO `sys_dept` (`id`, `name`, `code`, `parent_id`, `leader_id`, `level`, `path`, `contact_phone`, `address`, `description`, `status`) VALUES
(1, '总公司', 'HQ', NULL, 1, 1, '1', '010-88888888', '北京市朝阳区建国路88号', '集团总部', 1),
(2, '技术部', 'TECH', 1, 2, 2, '1,2', '010-88888801', '北京市朝阳区建国路88号A座5层', '负责技术研发', 1),
(3, '产品部', 'PRODUCT', 1, 3, 2, '1,3', '010-88888802', '北京市朝阳区建国路88号A座6层', '负责产品设计', 1),
(4, '运营部', 'OPERATION', 1, 4, 2, '1,4', '010-88888803', '北京市朝阳区建国路88号A座7层', '负责运营推广', 1),
(5, '人力资源部', 'HR', 1, 5, 2, '1,5', '010-88888804', '北京市朝阳区建国路88号B座3层', '负责人力资源', 1),
(6, '前端开发组', 'FE_DEV', 2, 6, 3, '1,2,6', '010-88888811', '北京市朝阳区建国路88号A座5层501', '负责前端开发', 1),
(7, '后端开发组', 'BE_DEV', 2, 7, 3, '1,2,7', '010-88888812', '北京市朝阳区建国路88号A座5层502', '负责后端开发', 1),
(8, '测试组', 'QA', 2, 8, 3, '1,2,8', '010-88888813', '北京市朝阳区建国路88号A座5层503', '负责质量保证', 1);

-- =============================================================
-- 2. 插入用户数据
-- 密码说明: 所有密码均为 bcrypt 加密后的 "123456"
-- =============================================================
INSERT INTO `sys_user` (`id`, `username`, `password`, `nickname`, `email`, `phone`, `avatar`, `department_id`, `status`, `last_login_time`, `last_login_ip`) VALUES
(1, 'admin', '$2b$12$32miI39znmr2o15ivWF8S.ozizj8JfDwnufI.nr0BXLiZ3Mwrqqu.', '系统管理员', 'admin@example.com', '13800138000', '/avatars/admin.jpg', 1, 1, NOW(), '127.0.0.1'),
(2, 'zhangsan', '$2b$12$32miI39znmr2o15ivWF8S.ozizj8JfDwnufI.nr0BXLiZ3Mwrqqu.', '张三', 'zhangsan@example.com', '13800138001', '/avatars/zhangsan.jpg', 2, 1, NULL, NULL),
(3, 'lisi', '$2b$12$32miI39znmr2o15ivWF8S.ozizj8JfDwnufI.nr0BXLiZ3Mwrqqu.', '李四', 'lisi@example.com', '13800138002', '/avatars/lisi.jpg', 3, 1, NULL, NULL),
(4, 'wangwu', '$2b$12$32miI39znmr2o15ivWF8S.ozizj8JfDwnufI.nr0BXLiZ3Mwrqqu.', '王五', 'wangwu@example.com', '13800138003', '/avatars/wangwu.jpg', 4, 1, NULL, NULL),
(5, 'zhaoliu', '$2b$12$32miI39znmr2o15ivWF8S.ozizj8JfDwnufI.nr0BXLiZ3Mwrqqu.', '赵六', 'zhaoliu@example.com', '13800138004', '/avatars/zhaoliu.jpg', 5, 1, NULL, NULL),
(6, 'qianqi', '$2b$12$32miI39znmr2o15ivWF8S.ozizj8JfDwnufI.nr0BXLiZ3Mwrqqu.', '钱七', 'qianqi@example.com', '13800138005', '/avatars/qianqi.jpg', 6, 1, NULL, NULL),
(7, 'sunba', '$2b$12$32miI39znmr2o15ivWF8S.ozizj8JfDwnufI.nr0BXLiZ3Mwrqqu.', '孙八', 'sunba@example.com', '13800138006', '/avatars/sunba.jpg', 7, 1, NULL, NULL),
(8, 'zhoujiu', '$2b$12$32miI39znmr2o15ivWF8S.ozizj8JfDwnufI.nr0BXLiZ3Mwrqqu.', '周九', 'zhoujiu@example.com', '13800138007', '/avatars/zhoujiu.jpg', 8, 1, NULL, NULL),
(9, 'wushi', '$2b$12$32miI39znmr2o15ivWF8S.ozizj8JfDwnufI.nr0BXLiZ3Mwrqqu.', '吴十', 'wushi@example.com', '13800138008', '/avatars/wushi.jpg', 6, 1, NULL, NULL),
(10, 'zhengyi', '$2b$12$32miI39znmr2o15ivWF8S.ozizj8JfDwnufI.nr0BXLiZ3Mwrqqu.', '郑一', 'zhengyi@example.com', '13800138009', '/avatars/zhengyi.jpg', 7, 0, NULL, NULL);

-- =============================================================
-- 3. 插入用户扩展信息
-- =============================================================
INSERT INTO `sys_user_profile` (`user_id`, `gender`, `birthday`, `id_card`, `address`, `emergency_contact`, `emergency_phone`, `position`, `entry_date`, `remark`) VALUES
(1, 1, '1985-01-15', '110101198501150011', '北京市海淀区中关村大街1号', '张夫人', '13900139000', 'CTO', '2015-01-01', '系统创始人'),
(2, 1, '1988-03-20', '110101198803200022', '北京市朝阳区望京SOHO', '李夫人', '13900139001', '技术总监', '2016-03-01', '技术部负责人'),
(3, 2, '1990-05-10', '110101199005100033', '北京市西城区金融街', '王先生', '13900139002', '产品总监', '2017-05-01', '产品部负责人'),
(4, 1, '1989-08-25', '110101198908250044', '北京市东城区王府井', '赵女士', '13900139003', '运营总监', '2016-08-01', '运营部负责人'),
(5, 2, '1991-11-08', '110101199111080055', '北京市丰台区丽泽商务区', '孙先生', '13900139004', '人力资源总监', '2018-01-01', '人力资源部负责人'),
(6, 1, '1993-02-14', '110101199302140066', '北京市通州区运河核心区', '周女士', '13900139005', '前端组长', '2019-02-01', '前端开发负责人'),
(7, 1, '1992-07-22', '110101199207220077', '北京市大兴区亦庄经济开发区', '吴女士', '13900139006', '后端组长', '2018-07-01', '后端开发负责人'),
(8, 2, '1994-12-03', '110101199412030088', '北京市昌平区回龙观', '郑先生', '13900139007', '测试组长', '2020-01-01', '测试负责人'),
(9, 1, '1995-04-30', '110101199504300099', '北京市顺义区后沙峪', '冯女士', '13900139008', '高级前端工程师', '2020-04-01', NULL),
(10, 2, '1996-09-18', '110101199609180100', '北京市房山区长阳', '陈先生', '13900139009', '高级后端工程师', '2021-01-01', '已离职');

-- =============================================================
-- 4. 插入角色数据
-- =============================================================
INSERT INTO `sys_role` (`id`, `name`, `code`, `parent_id`, `level`, `type`, `data_scope`, `sort`, `description`, `status`) VALUES
(1, '超级管理员', 'SUPER_ADMIN', NULL, 1, 0, 0, 1, '拥有系统所有权限', 1),
(2, '系统管理员', 'SYSTEM_ADMIN', 1, 2, 1, 0, 2, '系统管理权限', 1),
(3, '部门经理', 'DEPT_MANAGER', NULL, 1, 1, 2, 3, '部门管理权限', 1),
(4, '普通员工', 'EMPLOYEE', NULL, 1, 3, 3, 4, '普通员工权限', 1),
(5, '技术主管', 'TECH_LEAD', 3, 2, 1, 2, 1, '技术部主管', 1),
(6, '产品主管', 'PRODUCT_LEAD', 3, 2, 1, 2, 2, '产品部主管', 1),
(7, '前端开发工程师', 'FE_DEVELOPER', NULL, 1, 3, 3, 5, '前端开发权限', 1),
(8, '后端开发工程师', 'BE_DEVELOPER', NULL, 1, 3, 3, 6, '后端开发权限', 1),
(9, '测试工程师', 'QA_ENGINEER', NULL, 1, 3, 3, 7, '测试权限', 1),
(10, '访客', 'GUEST', NULL, 1, 3, 3, 10, '只读访客权限', 1);

-- =============================================================
-- 5. 插入用户角色关联
-- =============================================================
INSERT INTO `sys_user_role` (`user_id`, `role_id`, `is_primary`, `effective_time`, `expire_time`, `status`) VALUES
(1, 1, 1, NULL, NULL, 1),
(2, 2, 1, NULL, NULL, 1),
(2, 5, 0, NULL, NULL, 1),
(3, 2, 0, NULL, NULL, 1),
(3, 6, 1, NULL, NULL, 1),
(4, 3, 1, NULL, NULL, 1),
(5, 3, 1, NULL, NULL, 1),
(6, 5, 0, NULL, NULL, 1),
(6, 7, 1, NULL, NULL, 1),
(7, 5, 0, NULL, NULL, 1),
(7, 8, 1, NULL, NULL, 1),
(8, 9, 1, NULL, NULL, 1),
(9, 7, 1, NULL, NULL, 1),
(10, 8, 1, NULL, NULL, 1);

-- =============================================================
-- 6. 插入菜单数据
-- =============================================================
INSERT INTO `sys_menu` (`id`, `name`, `code`, `parent_id`, `level`, `type`, `path`, `component`, `icon`, `sort`, `status`) VALUES
(1, '系统管理', 'SYSTEM', NULL, 1, 0, '/system', NULL, 'setting', 1, 1),
(2, '用户管理', 'USER', 1, 2, 1, '/system/user', 'system/user/index', 'user', 1, 1),
(3, '角色管理', 'ROLE', 1, 2, 1, '/system/role', 'system/role/index', 'team', 2, 1),
(4, '权限管理', 'PERMISSION', 1, 2, 1, '/system/permission', 'system/permission/index', 'key', 3, 1),
(5, '菜单管理', 'MENU', 1, 2, 1, '/system/menu', 'system/menu/index', 'menu', 4, 1),
(6, '部门管理', 'DEPARTMENT', 1, 2, 1, '/system/department', 'system/department/index', 'apartment', 5, 1),
(7, '用户组管理', 'USER_GROUP', 1, 2, 1, '/system/user-group', 'system/user-group/index', 'usergroup', 6, 1),
(8, '系统监控', 'MONITOR', NULL, 1, 0, '/monitor', NULL, 'monitor', 2, 1),
(9, '在线用户', 'ONLINE_USER', 8, 2, 1, '/monitor/online', 'monitor/online/index', 'online', 1, 1),
(10, '操作日志', 'OPERATION_LOG', 8, 2, 1, '/monitor/operation-log', 'monitor/operation-log/index', 'log', 2, 1),
(11, '审计日志', 'AUDIT_LOG', 8, 2, 1, '/monitor/audit-log', 'monitor/audit-log/index', 'audit', 3, 1),
(12, '系统配置', 'CONFIG', NULL, 1, 0, '/config', NULL, 'config', 3, 1),
(13, '系统参数', 'SYSTEM_CONFIG', 12, 2, 1, '/config/system', 'config/system/index', 'parameter', 1, 1),
(14, '数据字典', 'DICT', 12, 2, 1, '/config/dict', 'config/dict/index', 'book', 2, 1),
(15, '个人中心', 'PROFILE', NULL, 1, 0, '/profile', NULL, 'user-center', 4, 1),
(16, '基本信息', 'BASIC_INFO', 15, 2, 1, '/profile/basic', 'profile/basic/index', 'info', 1, 1),
(17, '修改密码', 'CHANGE_PASSWORD', 15, 2, 1, '/profile/password', 'profile/password/index', 'lock', 2, 1);

-- =============================================================
-- 7. 插入权限数据
-- 注意：权限编码与后端API保持一致
-- =============================================================
INSERT INTO `sys_permission` (`id`, `name`, `code`, `type`, `resource_type`, `resource_id`, `action`, `path`, `method`, `parent_id`, `level`, `status`, `description`) VALUES
-- 用户管理权限
(1, '用户查询', 'user:view', 2, 'user', NULL, 'view', '/api/v1/users', 'GET', NULL, 1, 1, '查看用户列表和详情'),
(2, '创建用户', 'user:create', 2, 'user', NULL, 'create', '/api/v1/users', 'POST', 1, 2, 1, '创建新用户'),
(3, '更新用户', 'user:update', 2, 'user', NULL, 'update', '/api/v1/users/:id', 'PUT', 1, 2, 1, '更新用户信息'),
(4, '删除用户', 'user:delete', 2, 'user', NULL, 'delete', '/api/v1/users/:id', 'DELETE', 1, 2, 1, '删除用户'),
-- 角色管理权限
(5, '角色查询', 'role:view', 2, 'role', NULL, 'view', '/api/v1/roles', 'GET', NULL, 1, 1, '查看角色列表和详情'),
(6, '创建角色', 'role:create', 2, 'role', NULL, 'create', '/api/v1/roles', 'POST', 5, 2, 1, '创建新角色'),
(7, '更新角色', 'role:update', 2, 'role', NULL, 'update', '/api/v1/roles/:id', 'PUT', 5, 2, 1, '更新角色信息'),
(8, '删除角色', 'role:delete', 2, 'role', NULL, 'delete', '/api/v1/roles/:id', 'DELETE', 5, 2, 1, '删除角色'),
-- 权限管理权限
(9, '权限查询', 'permission:view', 2, 'permission', NULL, 'view', '/api/v1/permissions', 'GET', NULL, 1, 1, '查看权限列表和详情'),
(10, '创建权限', 'permission:create', 2, 'permission', NULL, 'create', '/api/v1/permissions', 'POST', 9, 2, 1, '创建新权限'),
(11, '更新权限', 'permission:update', 2, 'permission', NULL, 'update', '/api/v1/permissions/:id', 'PUT', 9, 2, 1, '更新权限信息'),
(12, '删除权限', 'permission:delete', 2, 'permission', NULL, 'delete', '/api/v1/permissions/:id', 'DELETE', 9, 2, 1, '删除权限'),
-- 菜单管理权限
(13, '菜单查询', 'menu:view', 2, 'menu', NULL, 'view', '/api/v1/menus', 'GET', NULL, 1, 1, '查看菜单列表和详情'),
(14, '创建菜单', 'menu:create', 2, 'menu', NULL, 'create', '/api/v1/menus', 'POST', 13, 2, 1, '创建菜单'),
(15, '更新菜单', 'menu:update', 2, 'menu', NULL, 'update', '/api/v1/menus/:id', 'PUT', 13, 2, 1, '更新菜单信息'),
(16, '删除菜单', 'menu:delete', 2, 'menu', NULL, 'delete', '/api/v1/menus/:id', 'DELETE', 13, 2, 1, '删除菜单'),
-- 部门管理权限
(17, '部门查询', 'department:view', 2, 'department', NULL, 'view', '/api/v1/departments', 'GET', NULL, 1, 1, '查看部门列表和详情'),
(18, '创建部门', 'department:create', 2, 'department', NULL, 'create', '/api/v1/departments', 'POST', 17, 2, 1, '创建新部门'),
(19, '更新部门', 'department:update', 2, 'department', NULL, 'update', '/api/v1/departments/:id', 'PUT', 17, 2, 1, '更新部门信息'),
(20, '删除部门', 'department:delete', 2, 'department', NULL, 'delete', '/api/v1/departments/:id', 'DELETE', 17, 2, 1, '删除部门'),
-- 用户组管理权限
(21, '用户组查询', 'user_group:view', 2, 'user_group', NULL, 'view', '/api/v1/user-groups', 'GET', NULL, 1, 1, '查看用户组列表和详情'),
(22, '创建用户组', 'user_group:create', 2, 'user_group', NULL, 'create', '/api/v1/user-groups', 'POST', 21, 2, 1, '创建新用户组'),
(23, '更新用户组', 'user_group:update', 2, 'user_group', NULL, 'update', '/api/v1/user-groups/:id', 'PUT', 21, 2, 1, '更新用户组信息'),
(24, '删除用户组', 'user_group:delete', 2, 'user_group', NULL, 'delete', '/api/v1/user-groups/:id', 'DELETE', 21, 2, 1, '删除用户组'),
-- 用户会话权限
(25, '会话查询', 'user_session:view', 2, 'user_session', NULL, 'view', '/api/v1/user-sessions', 'GET', NULL, 1, 1, '查看用户会话列表'),
(26, '会话更新', 'user_session:update', 2, 'user_session', NULL, 'update', '/api/v1/user-sessions/:id', 'PUT', 25, 2, 1, '更新用户会话'),
(27, '会话删除', 'user_session:delete', 2, 'user_session', NULL, 'delete', '/api/v1/user-sessions/:id', 'DELETE', 25, 2, 1, '删除用户会话'),
-- 用户资料权限
(28, '资料查询', 'user_profile:view', 2, 'user_profile', NULL, 'view', '/api/v1/user-profiles', 'GET', NULL, 1, 1, '查看用户资料'),
(29, '创建资料', 'user_profile:create', 2, 'user_profile', NULL, 'create', '/api/v1/user-profiles', 'POST', 28, 2, 1, '创建用户资料'),
(30, '更新资料', 'user_profile:update', 2, 'user_profile', NULL, 'update', '/api/v1/user-profiles/:id', 'PUT', 28, 2, 1, '更新用户资料'),
(31, '删除资料', 'user_profile:delete', 2, 'user_profile', NULL, 'delete', '/api/v1/user-profiles/:id', 'DELETE', 28, 2, 1, '删除用户资料'),
-- 操作日志权限
(32, '操作日志查询', 'log:view', 2, 'log', NULL, 'view', '/api/v1/operation-logs', 'GET', NULL, 1, 1, '查看操作日志'),
(33, '操作日志删除', 'log:delete', 2, 'log', NULL, 'delete', '/api/v1/operation-logs/cleanup', 'DELETE', 32, 2, 1, '清理操作日志'),
-- 审计日志权限
(34, '审计日志查询', 'audit:view', 2, 'audit', NULL, 'view', '/api/v1/audit-logs', 'GET', NULL, 1, 1, '查看审计日志'),
(35, '审计日志删除', 'audit:delete', 2, 'audit', NULL, 'delete', '/api/v1/audit-logs/cleanup', 'DELETE', 34, 2, 1, '清理审计日志'),
-- 字典管理权限
(36, '字典查询', 'dict:view', 2, 'dict', NULL, 'view', '/api/v1/dicts', 'GET', NULL, 1, 1, '查看字典列表和详情'),
(37, '创建字典', 'dict:create', 2, 'dict', NULL, 'create', '/api/v1/dicts', 'POST', 36, 2, 1, '创建字典'),
(38, '更新字典', 'dict:update', 2, 'dict', NULL, 'update', '/api/v1/dicts/:id', 'PUT', 36, 2, 1, '更新字典'),
(39, '删除字典', 'dict:delete', 2, 'dict', NULL, 'delete', '/api/v1/dicts/:id', 'DELETE', 36, 2, 1, '删除字典'),
-- 系统配置权限
(40, '配置查询', 'config:view', 2, 'config', NULL, 'view', '/api/v1/configs', 'GET', NULL, 1, 1, '查看系统配置'),
(41, '创建配置', 'config:create', 2, 'config', NULL, 'create', '/api/v1/configs', 'POST', 40, 2, 1, '创建系统配置'),
(42, '更新配置', 'config:update', 2, 'config', NULL, 'update', '/api/v1/configs/:id', 'PUT', 40, 2, 1, '更新系统配置'),
(43, '删除配置', 'config:delete', 2, 'config', NULL, 'delete', '/api/v1/configs/:id', 'DELETE', 40, 2, 1, '删除系统配置'),
-- 数据权限规则权限
(44, '数据权限查询', 'data_permission:view', 2, 'data_permission', NULL, 'view', '/api/v1/data-permission-rules', 'GET', NULL, 1, 1, '查看数据权限规则'),
(45, '创建数据权限', 'data_permission:create', 2, 'data_permission', NULL, 'create', '/api/v1/data-permission-rules', 'POST', 44, 2, 1, '创建数据权限规则'),
(46, '更新数据权限', 'data_permission:update', 2, 'data_permission', NULL, 'update', '/api/v1/data-permission-rules/:id', 'PUT', 44, 2, 1, '更新数据权限规则'),
(47, '删除数据权限', 'data_permission:delete', 2, 'data_permission', NULL, 'delete', '/api/v1/data-permission-rules/:id', 'DELETE', 44, 2, 1, '删除数据权限规则'),
-- 个人中心权限（基础权限 - 所有用户都应该有）
(48, '查看个人信息', 'profile:view', 2, 'profile', NULL, 'view', '/api/v1/profile', 'GET', NULL, 1, 1, '查看个人信息'),
(49, '更新个人信息', 'profile:update', 2, 'profile', NULL, 'update', '/api/v1/profile', 'PUT', 48, 2, 1, '更新个人信息'),
(50, '修改密码', 'profile:change-password', 2, 'profile', NULL, 'update', '/api/v1/profile/password', 'PUT', 48, 2, 1, '修改密码');

-- =============================================================
-- 8. 插入菜单权限关联
-- =============================================================
INSERT INTO `sys_menu_permission` (`menu_id`, `permission_id`, `status`) VALUES
(2, 1, 1), (2, 2, 1), (2, 3, 1), (2, 4, 1),
(3, 5, 1), (3, 6, 1), (3, 7, 1), (3, 8, 1),
(4, 9, 1), (4, 10, 1), (4, 11, 1), (4, 12, 1),
(5, 13, 1), (5, 14, 1), (5, 15, 1), (5, 16, 1),
(6, 17, 1), (6, 18, 1), (6, 19, 1), (6, 20, 1),
(7, 21, 1), (7, 22, 1), (7, 23, 1), (7, 24, 1),
(9, 25, 1), (9, 26, 1), (9, 27, 1),
(10, 32, 1), (10, 33, 1),
(11, 34, 1), (11, 35, 1),
(13, 40, 1), (13, 41, 1), (13, 42, 1), (13, 43, 1),
(14, 36, 1), (14, 37, 1), (14, 38, 1), (14, 39, 1),
(16, 48, 1), (16, 49, 1),
(17, 50, 1);

-- =============================================================
-- 9. 插入角色权限关联
-- 超级管理员拥有所有权限
-- =============================================================
-- 超级管理员 - 所有权限
INSERT INTO `sys_role_permission` (`role_id`, `permission_id`, `status`)
SELECT 1, id, 1 FROM `sys_permission`;

-- 系统管理员 - 大部分管理权限（排除一些敏感权限）
INSERT INTO `sys_role_permission` (`role_id`, `permission_id`, `status`)
SELECT 2, id, 1 FROM `sys_permission` WHERE id NOT IN (27, 31, 35, 43, 47);

-- 部门经理 - 部门相关权限
INSERT INTO `sys_role_permission` (`role_id`, `permission_id`, `status`) VALUES
(3, 1, 1), (3, 3, 1),
(3, 17, 1), (3, 19, 1),
(3, 32, 1),
(3, 48, 1), (3, 49, 1), (3, 50, 1);

-- 普通员工 - 基础权限
INSERT INTO `sys_role_permission` (`role_id`, `permission_id`, `status`) VALUES
(4, 48, 1), (4, 49, 1), (4, 50, 1);

-- 技术主管 - 技术部门管理权限
INSERT INTO `sys_role_permission` (`role_id`, `permission_id`, `status`)
SELECT 5, id, 1 FROM `sys_permission` WHERE id IN (1, 3, 5, 7, 17, 19, 32, 48, 49, 50);

-- 产品主管 - 产品部门管理权限
INSERT INTO `sys_role_permission` (`role_id`, `permission_id`, `status`)
SELECT 6, id, 1 FROM `sys_permission` WHERE id IN (1, 3, 5, 7, 17, 19, 32, 48, 49, 50);

-- 前端开发工程师
INSERT INTO `sys_role_permission` (`role_id`, `permission_id`, `status`) VALUES
(7, 48, 1), (7, 49, 1), (7, 50, 1);

-- 后端开发工程师
INSERT INTO `sys_role_permission` (`role_id`, `permission_id`, `status`) VALUES
(8, 48, 1), (8, 49, 1), (8, 50, 1);

-- 测试工程师
INSERT INTO `sys_role_permission` (`role_id`, `permission_id`, `status`) VALUES
(9, 48, 1), (9, 49, 1), (9, 50, 1);

-- 访客 - 只读权限
INSERT INTO `sys_role_permission` (`role_id`, `permission_id`, `status`) VALUES
(10, 48, 1);

-- =============================================================
-- 10. 插入用户组数据
-- =============================================================
INSERT INTO `sys_user_group` (`id`, `name`, `code`, `description`, `status`, `sort`) VALUES
(1, '管理员组', 'ADMIN_GROUP', '系统管理员用户组', 1, 1),
(2, '技术团队', 'TECH_TEAM', '技术部全体员工', 1, 2),
(3, '产品团队', 'PRODUCT_TEAM', '产品部全体员工', 1, 3),
(4, '开发团队', 'DEV_TEAM', '前端和后端开发人员', 1, 4),
(5, '测试团队', 'QA_TEAM', '测试人员', 1, 5);

-- =============================================================
-- 11. 插入用户组-用户关联
-- =============================================================
INSERT INTO `sys_user_group_relation` (`user_group_id`, `user_id`, `status`) VALUES
(1, 1, 1), (1, 2, 1),
(2, 2, 1), (2, 6, 1), (2, 7, 1), (2, 8, 1), (2, 9, 1), (2, 10, 1),
(3, 3, 1),
(4, 6, 1), (4, 7, 1), (4, 9, 1), (4, 10, 1),
(5, 8, 1);

-- =============================================================
-- 12. 插入用户组-角色关联
-- =============================================================
INSERT INTO `sys_user_group_role_relation` (`user_group_id`, `role_id`, `status`) VALUES
(1, 1, 1), (1, 2, 1),
(2, 5, 1),
(3, 6, 1),
(4, 7, 1), (4, 8, 1),
(5, 9, 1);

-- =============================================================
-- 13. 插入数据权限规则
-- =============================================================
INSERT INTO `sys_data_permission_rule` (`name`, `code`, `permission_id`, `resource_table`, `rule_type`, `rule_expression`, `status`, `description`) VALUES
('全部数据', 'ALL_DATA', 1, 'sys_user', 0, NULL, 1, '可以查看所有用户数据'),
('本部门数据', 'DEPT_DATA', 1, 'sys_user', 1, 'department_id = {current_user_department_id}', 1, '只能查看本部门用户数据'),
('本部门及下级数据', 'DEPT_AND_CHILD_DATA', 1, 'sys_user', 2, 'department_id IN ({current_user_department_ids})', 1, '可以查看本部门及下级部门用户数据'),
('仅本人数据', 'SELF_DATA', 1, 'sys_user', 3, 'id = {current_user_id}', 1, '只能查看自己的数据');

-- =============================================================
-- 14. 更新系统配置（增加更多配置项）
-- =============================================================
INSERT INTO `sys_config` (`config_key`, `config_value`, `config_type`, `description`, `group_name`, `is_system`, `status`, `sort`) VALUES
('site.copyright', 'Copyright © 2026 RBAC System', 'string', '版权信息', 'basic', 1, 1, 4),
('site.icp', '京ICP备12345678号', 'string', 'ICP备案号', 'basic', 1, 1, 5),
('user.allow_register', 'false', 'bool', '是否允许用户注册', 'user', 1, 1, 1),
('user.default_role', '4', 'int', '新用户默认角色ID', 'user', 1, 1, 2),
('user.account_lock_threshold', '5', 'int', '账户锁定阈值（登录失败次数）', 'security', 1, 1, 4),
('user.account_lock_duration', '30', 'int', '账户锁定时长（分钟）', 'security', 1, 1, 5),
('log.operation_retention_days', '90', 'int', '操作日志保留天数', 'log', 1, 1, 1),
('log.audit_retention_days', '365', 'int', '审计日志保留天数', 'log', 1, 1, 2);

-- =============================================================
-- 15. 插入更多系统字典项
-- =============================================================
INSERT INTO `sys_dict` (`name`, `code`, `description`, `status`, `sort`) VALUES
('数据范围', 'data_scope', '数据权限范围', 1, 6),
('菜单类型', 'menu_type_ext', '菜单类型扩展', 1, 7);

INSERT INTO `sys_dict_item` (`dict_id`, `label`, `value`, `sort`) VALUES
(6, '全部数据', '0', 1),
(6, '本部门数据', '1', 2),
(6, '本部门及下级数据', '2', 3),
(6, '仅本人数据', '3', 4),
(6, '自定义数据', '4', 5),
(7, '目录', '0', 1),
(7, '菜单', '1', 2),
(7, '按钮', '2', 3),
(7, '内嵌', '3', 4),
(7, '外链', '4', 5);

-- =============================================================
-- 16. 插入操作日志示例数据
-- =============================================================
INSERT INTO `sys_operation_log` (`user_id`, `username`, `module`, `operation`, `description`, `request_method`, `request_url`, `request_params`, `response_result`, `execution_time`, `ip_address`, `user_agent`, `status`, `error_message`) VALUES
(1, 'admin', '用户管理', '登录', '用户登录系统', 'POST', '/api/v1/auth/login', '{"username":"admin"}', '{"code":200,"message":"success"}', 120, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 1, NULL),
(1, 'admin', '用户管理', '查询列表', '查询用户列表', 'GET', '/api/v1/users', '{"page":1,"size":10}', '{"code":200,"data":{"total":10}}', 85, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 1, NULL),
(1, 'admin', '角色管理', '创建角色', '创建新角色', 'POST', '/api/v1/roles', '{"name":"测试角色"}', '{"code":200,"data":{"id":11}}', 200, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 1, NULL),
(2, 'zhangsan', '个人中心', '修改密码', '修改登录密码', 'PUT', '/api/v1/profile/password', '{}', '{"code":200,"message":"success"}', 150, '192.168.1.100', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)', 1, NULL),
(1, 'admin', '系统配置', '更新配置', '更新系统配置参数', 'PUT', '/api/v1/configs/1', '{"config_value":"新的系统名称"}', '{"code":200,"message":"success"}', 90, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 1, NULL);

-- =============================================================
-- 17. 插入审计日志示例数据
-- =============================================================
INSERT INTO `sys_audit_log` (`table_name`, `record_id`, `operation_type`, `field_name`, `old_value`, `new_value`, `user_id`, `username`, `change_reason`) VALUES
('sys_user', 2, 'UPDATE', 'nickname', '张三', '张三丰', 1, 'admin', '用户要求修改昵称'),
('sys_user', 3, 'UPDATE', 'status', '0', '1', 1, 'admin', '启用用户账户'),
('sys_role', 3, 'UPDATE', 'description', '部门管理权限', '部门经理拥有部门管理和查看权限', 1, 'admin', '完善角色描述'),
('sys_config', 1, 'UPDATE', 'config_value', '企业级RBAC系统', '企业级权限管理系统', 1, 'admin', '系统名称调整');

SET FOREIGN_KEY_CHECKS = 1;

-- =============================================================
-- 演示数据脚本执行完成
-- =============================================================
-- 管理员账号: admin / 123456
-- =============================================================
