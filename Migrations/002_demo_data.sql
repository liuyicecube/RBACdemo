-- ============================================
-- 企业级RBAC系统 - 演示数据
-- 版本: v2.1
-- 描述: 与 SQLAlchemy 模型完美匹配的丰富演示数据
-- ============================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================
-- 1. 用户数据
-- ============================================
INSERT INTO `sys_user` (`id`, `username`, `password`, `nickname`, `email`, `phone`, `avatar`, `department_id`, `status`, `last_login_time`, `last_login_ip`, `tenant_id`, `create_time`, `update_time`, `is_deleted`, `version`) VALUES
(1, 'admin', '$2b$12$32miI39znmr2o15ivWF8S.ozizj8JfDwnufI.nr0BXLiZ3Mwrqqu.', '系统管理员', 'admin@example.com', '13800000001', NULL, 1, 1, NULL, NULL, 1, NOW(), NOW(), 0, 1),
(2, 'zhangsan', '$2b$12$Xf7sAOPi1C9Uv6hUdnDK2ecHO5231XcUIR4uNrMH0CbahK0Ej0PgO', '张三', 'zhangsan@example.com', '13800000002', NULL, 2, 1, NULL, NULL, 1, NOW(), NOW(), 0, 1),
(3, 'lisi', '$2b$12$YXscLkwzSSDagweSLc6NJObvC3ZLwMKmMQK/5tcZcXMzSWUXEumQy', '李四', 'lisi@example.com', '13800000003', NULL, 2, 1, NULL, NULL, 1, NOW(), NOW(), 0, 1),
(4, 'wangwu', '$2b$12$eDPuGotdFQqYx9yx6caWsuixK07QlOkdN9XPBfarW7rfKCI.PF86i', '王五', 'wangwu@example.com', '13800000004', NULL, 3, 1, NULL, NULL, 1, NOW(), NOW(), 0, 1),
(5, 'zhaoliu', '$2b$12$HPGfZZdUUIuS3uPRboaTperWK3sJOugbht6eEDp5ZBDzHnE0gRz.u', '赵六', 'zhaoliu@example.com', '13800000005', NULL, 3, 1, NULL, NULL, 1, NOW(), NOW(), 0, 1),
(6, 'sunqi', '$2b$12$fEhw3mfonRAFi/ZydOkQdeWACav43QFBb3Tanjb38e9YY3Xep/V/e', '孙七', 'sunqi@example.com', '13800000006', NULL, 4, 1, NULL, NULL, 1, NOW(), NOW(), 0, 1),
(7, 'zhouba', '$2b$12$b73imfp3c/xH4Xl/kBDUgua1pp5OVV9GhiZW0aISHG8aZTrCr4msy', '周八', 'zhouba@example.com', '13800000007', NULL, 5, 1, NULL, NULL, 1, NOW(), NOW(), 0, 1),
(8, 'wujiu', '$2b$12$BIObQ8vnCwE6oqO7hLI93e8hrpb9MEep2sK6eXepfE.6eb6SJHTYG', '吴九', 'wujiu@example.com', '13800000008', NULL, 6, 1, NULL, NULL, 1, NOW(), NOW(), 0, 1),
(9, 'zhengshi', '$2b$12$Ds72MeQfaRlYWJcNig2MtuJBHebNQtJTn8HK76MTyUnR/GRoiBxYG', '郑十', 'zhengshi@example.com', '13800000009', NULL, 4, 1, NULL, NULL, 1, NOW(), NOW(), 0, 1),
(10, 'qianyi', '$2b$12$dF5JjPVx4DEV/7v25zSytOr.6XeNYTwV1gYh4xcAUc6OW90/67/w6', '钱一', 'qianyi@example.com', '13800000010', NULL, 5, 1, NULL, NULL, 1, NOW(), NOW(), 0, 1);

-- ============================================
-- 2. 用户扩展信息
-- ============================================
INSERT INTO `sys_user_profile` (`id`, `user_id`, `gender`, `birthday`, `id_card`, `address`, `emergency_contact`, `emergency_phone`, `position`, `entry_date`, `remark`, `tenant_id`, `create_time`, `update_time`, `is_deleted`, `version`) VALUES
(1, 1, 1, '1985-05-10', '110101198505100001', '北京市朝阳区建国路88号', '张总', '13900000001', '系统管理员', '2020-01-01', '负责系统整体运维管理', 1, NOW(), NOW(), 0, 1),
(2, 2, 1, '1990-03-15', '110101199003150002', '北京市海淀区中关村大街1号', '李总', '13900000002', '技术总监', '2020-06-15', '负责技术部全面工作', 1, NOW(), NOW(), 0, 1),
(3, 3, 1, '1992-08-20', '110101199208200003', '北京市西城区金融街10号', '王总', '13900000003', '高级开发工程师', '2021-02-20', '负责后端开发工作', 1, NOW(), NOW(), 0, 1),
(4, 4, 2, '1988-12-08', '110101198812080004', '北京市东城区王府井大街1号', '赵总', '13900000004', '市场总监', '2020-09-01', '负责市场部全面工作', 1, NOW(), NOW(), 0, 1),
(5, 5, 1, '1995-06-25', '110101199506250005', '北京市丰台区南三环西路5号', '孙总', '13900000005', '市场经理', '2022-01-10', '负责市场推广工作', 1, NOW(), NOW(), 0, 1);

-- ============================================
-- 3. 角色数据
-- ============================================
INSERT INTO `sys_role` (`id`, `name`, `code`, `parent_id`, `level`, `type`, `data_scope`, `sort`, `description`, `status`, `tenant_id`, `create_time`, `update_time`, `is_deleted`, `version`) VALUES
(1, '超级管理员', 'super_admin', NULL, 1, 0, 0, 1, '系统超级管理员，拥有所有权限', 1, 1, NOW(), NOW(), 0, 1),
(2, '系统管理员', 'admin', 1, 2, 0, 0, 2, '系统管理员，管理系统配置', 1, 1, NOW(), NOW(), 0, 1),
(3, '部门经理', 'dept_manager', NULL, 1, 1, 2, 3, '部门经理，管理本部门及下级数据', 1, 1, NOW(), NOW(), 0, 1),
(4, '普通员工', 'staff', NULL, 1, 1, 3, 4, '普通员工，只能查看和管理本人数据', 1, 1, NOW(), NOW(), 0, 1),
(5, '技术开发', 'tech_dev', NULL, 1, 1, 1, 5, '技术开发人员，负责系统开发', 1, 1, NOW(), NOW(), 0, 1),
(6, '市场专员', 'marketing', NULL, 1, 1, 2, 6, '市场专员，负责市场相关工作', 1, 1, NOW(), NOW(), 0, 1);

-- ============================================
-- 4. 用户-角色关联
-- ============================================
INSERT INTO `sys_user_role` (`id`, `user_id`, `role_id`, `is_primary`, `status`, `tenant_id`, `create_time`, `update_time`, `is_deleted`, `version`) VALUES
(1, 1, 1, 1, 1, 1, NOW(), NOW(), 0, 1),
(2, 2, 3, 1, 1, 1, NOW(), NOW(), 0, 1),
(3, 2, 5, 0, 1, 1, NOW(), NOW(), 0, 1),
(4, 3, 5, 1, 1, 1, NOW(), NOW(), 0, 1),
(5, 4, 3, 1, 1, 1, NOW(), NOW(), 0, 1),
(6, 4, 6, 0, 1, 1, NOW(), NOW(), 0, 1),
(7, 5, 6, 1, 1, 1, NOW(), NOW(), 0, 1),
(8, 6, 5, 1, 1, 1, NOW(), NOW(), 0, 1),
(9, 7, 6, 1, 1, 1, NOW(), NOW(), 0, 1),
(10, 8, 4, 1, 1, 1, NOW(), NOW(), 0, 1),
(11, 9, 5, 1, 1, 1, NOW(), NOW(), 0, 1),
(12, 10, 4, 1, 1, 1, NOW(), NOW(), 0, 1);

-- ============================================
-- 5. 部门数据
-- ============================================
INSERT INTO `sys_dept` (`id`, `name`, `code`, `parent_id`, `leader_id`, `level`, `path`, `contact_phone`, `address`, `description`, `status`, `tenant_id`, `create_time`, `update_time`, `is_deleted`, `version`) VALUES
(1, '总公司', 'hq', NULL, 1, 1, '1', '010-88888888', '北京市朝阳区xxx路1号', '总公司', 1, 1, NOW(), NOW(), 0, 1),
(2, '技术部', 'tech', 1, 2, 2, '1,2', '010-88888801', '技术部办公室', '负责技术研发', 1, 1, NOW(), NOW(), 0, 1),
(3, '市场部', 'market', 1, 4, 2, '1,3', '010-88888802', '市场部办公室', '负责市场推广', 1, 1, NOW(), NOW(), 0, 1),
(4, '后端开发组', 'backend', 2, 3, 3, '1,2,4', '010-88888803', '后端开发组办公室', '负责后端系统开发', 1, 1, NOW(), NOW(), 0, 1),
(5, '前端开发组', 'frontend', 2, 6, 3, '1,2,5', '010-88888804', '前端开发组办公室', '负责前端系统开发', 1, 1, NOW(), NOW(), 0, 1),
(6, '销售组', 'sales', 3, 5, 3, '1,3,6', '010-88888805', '销售组办公室', '负责销售业务', 1, 1, NOW(), NOW(), 0, 1);

-- ============================================
-- 6. 用户组数据
-- ============================================
INSERT INTO `sys_user_group` (`id`, `name`, `code`, `description`, `sort`, `status`, `tenant_id`, `create_time`, `update_time`, `is_deleted`, `version`) VALUES
(1, '技术团队', 'tech_team', '公司技术团队', 1, 1, 1, NOW(), NOW(), 0, 1),
(2, '市场团队', 'market_team', '公司市场团队', 2, 1, 1, NOW(), NOW(), 0, 1),
(3, '管理层', 'management', '公司管理层', 3, 1, 1, NOW(), NOW(), 0, 1),
(4, '新员工', 'new_staff', '公司新入职员工', 4, 1, 1, NOW(), NOW(), 0, 1);

-- ============================================
-- 7. 用户组-用户关联
-- ============================================
INSERT INTO `sys_user_group_relation` (`id`, `user_group_id`, `user_id`, `status`, `tenant_id`, `create_time`, `update_time`, `is_deleted`, `version`) VALUES
(1, 1, 2, 1, 1, NOW(), NOW(), 0, 1),
(2, 1, 3, 1, 1, NOW(), NOW(), 0, 1),
(3, 1, 6, 1, 1, NOW(), NOW(), 0, 1),
(4, 1, 9, 1, 1, NOW(), NOW(), 0, 1),
(5, 2, 4, 1, 1, NOW(), NOW(), 0, 1),
(6, 2, 5, 1, 1, NOW(), NOW(), 0, 1),
(7, 2, 7, 1, 1, NOW(), NOW(), 0, 1),
(8, 3, 1, 1, 1, NOW(), NOW(), 0, 1),
(9, 3, 2, 1, 1, NOW(), NOW(), 0, 1),
(10, 3, 4, 1, 1, NOW(), NOW(), 0, 1),
(11, 4, 8, 1, 1, NOW(), NOW(), 0, 1),
(12, 4, 10, 1, 1, NOW(), NOW(), 0, 1);

-- ============================================
-- 8. 用户组-角色关联
-- ============================================
INSERT INTO `sys_user_group_role_relation` (`id`, `user_group_id`, `role_id`, `status`, `tenant_id`, `create_time`, `update_time`, `is_deleted`, `version`) VALUES
(1, 1, 5, 1, 1, NOW(), NOW(), 0, 1),
(2, 2, 6, 1, 1, NOW(), NOW(), 0, 1),
(3, 3, 3, 1, 1, NOW(), NOW(), 0, 1),
(4, 4, 4, 1, 1, NOW(), NOW(), 0, 1);

-- ============================================
-- 9. 菜单数据
-- ============================================
INSERT INTO `sys_menu` (`id`, `name`, `code`, `parent_id`, `level`, `type`, `path`, `component`, `icon`, `sort`, `status`, `tenant_id`, `create_time`, `update_time`, `is_deleted`, `version`) VALUES
(1, '首页', 'dashboard', NULL, 1, 1, '/dashboard', 'dashboard/index', 'HomeOutlined', 1, 1, 1, NOW(), NOW(), 0, 1),
(2, '系统管理', 'system', NULL, 1, 0, '/system', NULL, 'SettingOutlined', 2, 1, 1, NOW(), NOW(), 0, 1),
(3, '用户管理', 'system:user', 2, 2, 1, '/system/user', 'system/user/index', 'UserOutlined', 1, 1, 1, NOW(), NOW(), 0, 1),
(4, '角色管理', 'system:role', 2, 2, 1, '/system/role', 'system/role/index', 'TeamOutlined', 2, 1, 1, NOW(), NOW(), 0, 1),
(5, '菜单管理', 'system:menu', 2, 2, 1, '/system/menu', 'system/menu/index', 'MenuOutlined', 3, 1, 1, NOW(), NOW(), 0, 1),
(6, '部门管理', 'system:dept', 2, 2, 1, '/system/dept', 'system/dept/index', 'ApartmentOutlined', 4, 1, 1, NOW(), NOW(), 0, 1),
(7, '用户组管理', 'system:user_group', 2, 2, 1, '/system/user-group', 'system/user-group/index', 'UsergroupAddOutlined', 5, 1, 1, NOW(), NOW(), 0, 1),
(8, '系统设置', 'system:settings', 2, 2, 0, NULL, NULL, 'ToolOutlined', 6, 1, 1, NOW(), NOW(), 0, 1),
(9, '字典管理', 'system:dict', 8, 3, 1, '/system/dict', 'system/dict/index', 'BookOutlined', 1, 1, 1, NOW(), NOW(), 0, 1),
(10, '系统配置', 'system:config', 8, 3, 1, '/system/config', 'system/config/index', 'SettingOutlined', 2, 1, 1, NOW(), NOW(), 0, 1),
(11, '日志管理', 'system:log', 2, 2, 0, NULL, NULL, 'FileTextOutlined', 7, 1, 1, NOW(), NOW(), 0, 1),
(12, '操作日志', 'system:operation_log', 11, 3, 1, '/system/operation-log', 'system/operation-log/index', 'HistoryOutlined', 1, 1, 1, NOW(), NOW(), 0, 1),
(13, '审计日志', 'system:audit_log', 11, 3, 1, '/system/audit-log', 'system/audit-log/index', 'AuditOutlined', 2, 1, 1, NOW(), NOW(), 0, 1);

-- ============================================
-- ============================================
-- 10. 权限数据
-- ============================================
INSERT INTO `sys_permission` (`id`, `name`, `code`, `type`, `resource_type`, `action`, `status`, `tenant_id`, `create_time`, `update_time`, `is_deleted`, `version`) VALUES
(1, '查看用户', 'user:view', 2, 'user', 'view', 1, 1, NOW(), NOW(), 0, 1),
(2, '创建用户', 'user:create', 2, 'user', 'create', 1, 1, NOW(), NOW(), 0, 1),
(3, '更新用户', 'user:update', 2, 'user', 'update', 1, 1, NOW(), NOW(), 0, 1),
(4, '删除用户', 'user:delete', 2, 'user', 'delete', 1, 1, NOW(), NOW(), 0, 1),
(5, '查看角色', 'role:view', 2, 'role', 'view', 1, 1, NOW(), NOW(), 0, 1),
(6, '创建角色', 'role:create', 2, 'role', 'create', 1, 1, NOW(), NOW(), 0, 1),
(7, '更新角色', 'role:update', 2, 'role', 'update', 1, 1, NOW(), NOW(), 0, 1),
(8, '删除角色', 'role:delete', 2, 'role', 'delete', 1, 1, NOW(), NOW(), 0, 1),
(9, '查看权限', 'permission:view', 2, 'permission', 'view', 1, 1, NOW(), NOW(), 0, 1),
(10, '创建权限', 'permission:create', 2, 'permission', 'create', 1, 1, NOW(), NOW(), 0, 1),
(11, '更新权限', 'permission:update', 2, 'permission', 'update', 1, 1, NOW(), NOW(), 0, 1),
(12, '删除权限', 'permission:delete', 2, 'permission', 'delete', 1, 1, NOW(), NOW(), 0, 1),
(13, '查看菜单', 'menu:view', 2, 'menu', 'view', 1, 1, NOW(), NOW(), 0, 1),
(14, '创建菜单', 'menu:create', 2, 'menu', 'create', 1, 1, NOW(), NOW(), 0, 1),
(15, '更新菜单', 'menu:update', 2, 'menu', 'update', 1, 1, NOW(), NOW(), 0, 1),
(16, '删除菜单', 'menu:delete', 2, 'menu', 'delete', 1, 1, NOW(), NOW(), 0, 1),
(17, '查看部门', 'department:view', 2, 'department', 'view', 1, 1, NOW(), NOW(), 0, 1),
(18, '创建部门', 'department:create', 2, 'department', 'create', 1, 1, NOW(), NOW(), 0, 1),
(19, '更新部门', 'department:update', 2, 'department', 'update', 1, 1, NOW(), NOW(), 0, 1),
(20, '删除部门', 'department:delete', 2, 'department', 'delete', 1, 1, NOW(), NOW(), 0, 1),
(21, '查看用户组', 'user_group:view', 2, 'user_group', 'view', 1, 1, NOW(), NOW(), 0, 1),
(22, '创建用户组', 'user_group:create', 2, 'user_group', 'create', 1, 1, NOW(), NOW(), 0, 1),
(23, '更新用户组', 'user_group:update', 2, 'user_group', 'update', 1, 1, NOW(), NOW(), 0, 1),
(24, '删除用户组', 'user_group:delete', 2, 'user_group', 'delete', 1, 1, NOW(), NOW(), 0, 1),
(25, '查看用户会话', 'user_session:view', 2, 'user_session', 'view', 1, 1, NOW(), NOW(), 0, 1),
(26, '更新用户会话', 'user_session:update', 2, 'user_session', 'update', 1, 1, NOW(), NOW(), 0, 1),
(27, '删除用户会话', 'user_session:delete', 2, 'user_session', 'delete', 1, 1, NOW(), NOW(), 0, 1),
(28, '查看用户资料', 'user_profile:view', 2, 'user_profile', 'view', 1, 1, NOW(), NOW(), 0, 1),
(29, '创建用户资料', 'user_profile:create', 2, 'user_profile', 'create', 1, 1, NOW(), NOW(), 0, 1),
(30, '更新用户资料', 'user_profile:update', 2, 'user_profile', 'update', 1, 1, NOW(), NOW(), 0, 1),
(31, '删除用户资料', 'user_profile:delete', 2, 'user_profile', 'delete', 1, 1, NOW(), NOW(), 0, 1),
(32, '查看字典', 'dict:view', 2, 'dict', 'view', 1, 1, NOW(), NOW(), 0, 1),
(33, '创建字典', 'dict:create', 2, 'dict', 'create', 1, 1, NOW(), NOW(), 0, 1),
(34, '更新字典', 'dict:update', 2, 'dict', 'update', 1, 1, NOW(), NOW(), 0, 1),
(35, '删除字典', 'dict:delete', 2, 'dict', 'delete', 1, 1, NOW(), NOW(), 0, 1),
(36, '查看配置', 'config:view', 2, 'config', 'view', 1, 1, NOW(), NOW(), 0, 1),
(37, '创建配置', 'config:create', 2, 'config', 'create', 1, 1, NOW(), NOW(), 0, 1),
(38, '更新配置', 'config:update', 2, 'config', 'update', 1, 1, NOW(), NOW(), 0, 1),
(39, '删除配置', 'config:delete', 2, 'config', 'delete', 1, 1, NOW(), NOW(), 0, 1);

-- ============================================
-- 11. 角色-权限关联
-- ============================================
INSERT INTO `sys_role_permission` (`id`, `role_id`, `permission_id`, `status`, `tenant_id`, `create_time`, `update_time`, `is_deleted`, `version`) VALUES
(1, 1, 1, 1, 1, NOW(), NOW(), 0, 1),
(2, 1, 2, 1, 1, NOW(), NOW(), 0, 1),
(3, 1, 3, 1, 1, NOW(), NOW(), 0, 1),
(4, 1, 4, 1, 1, NOW(), NOW(), 0, 1),
(5, 1, 5, 1, 1, NOW(), NOW(), 0, 1),
(6, 1, 6, 1, 1, NOW(), NOW(), 0, 1),
(7, 1, 7, 1, 1, NOW(), NOW(), 0, 1),
(8, 1, 8, 1, 1, NOW(), NOW(), 0, 1),
(9, 1, 9, 1, 1, NOW(), NOW(), 0, 1),
(10, 1, 10, 1, 1, NOW(), NOW(), 0, 1),
(11, 1, 11, 1, 1, NOW(), NOW(), 0, 1),
(12, 1, 12, 1, 1, NOW(), NOW(), 0, 1),
(13, 1, 13, 1, 1, NOW(), NOW(), 0, 1),
(14, 1, 14, 1, 1, NOW(), NOW(), 0, 1),
(15, 1, 15, 1, 1, NOW(), NOW(), 0, 1),
(16, 1, 16, 1, 1, NOW(), NOW(), 0, 1),
(17, 1, 17, 1, 1, NOW(), NOW(), 0, 1),
(18, 1, 18, 1, 1, NOW(), NOW(), 0, 1),
(19, 1, 19, 1, 1, NOW(), NOW(), 0, 1),
(20, 1, 20, 1, 1, NOW(), NOW(), 0, 1),
(21, 1, 21, 1, 1, NOW(), NOW(), 0, 1),
(22, 1, 22, 1, 1, NOW(), NOW(), 0, 1),
(23, 1, 23, 1, 1, NOW(), NOW(), 0, 1),
(24, 1, 24, 1, 1, NOW(), NOW(), 0, 1),
(25, 1, 25, 1, 1, NOW(), NOW(), 0, 1),
(26, 1, 26, 1, 1, NOW(), NOW(), 0, 1),
(27, 1, 27, 1, 1, NOW(), NOW(), 0, 1),
(28, 1, 28, 1, 1, NOW(), NOW(), 0, 1),
(29, 1, 29, 1, 1, NOW(), NOW(), 0, 1),
(30, 1, 30, 1, 1, NOW(), NOW(), 0, 1),
(31, 1, 31, 1, 1, NOW(), NOW(), 0, 1),
(32, 1, 32, 1, 1, NOW(), NOW(), 0, 1),
(33, 1, 33, 1, 1, NOW(), NOW(), 0, 1),
(34, 1, 34, 1, 1, NOW(), NOW(), 0, 1),
(35, 1, 35, 1, 1, NOW(), NOW(), 0, 1),
(36, 1, 36, 1, 1, NOW(), NOW(), 0, 1),
(37, 1, 37, 1, 1, NOW(), NOW(), 0, 1),
(38, 1, 38, 1, 1, NOW(), NOW(), 0, 1),
(39, 1, 39, 1, 1, NOW(), NOW(), 0, 1);
-- 12. 菜单-权限关联
-- ============================================
INSERT INTO `sys_menu_permission` (`id`, `menu_id`, `permission_id`, `status`, `tenant_id`, `create_time`, `update_time`, `is_deleted`, `version`) VALUES
(1, 3, 1, 1, 1, NOW(), NOW(), 0, 1),
(2, 3, 2, 1, 1, NOW(), NOW(), 0, 1),
(3, 3, 3, 1, 1, NOW(), NOW(), 0, 1),
(4, 3, 4, 1, 1, NOW(), NOW(), 0, 1),
(5, 4, 5, 1, 1, NOW(), NOW(), 0, 1),
(6, 4, 6, 1, 1, NOW(), NOW(), 0, 1),
(7, 4, 7, 1, 1, NOW(), NOW(), 0, 1),
(8, 4, 8, 1, 1, NOW(), NOW(), 0, 1),
(9, 5, 9, 1, 1, NOW(), NOW(), 0, 1),
(10, 5, 10, 1, 1, NOW(), NOW(), 0, 1),
(11, 5, 11, 1, 1, NOW(), NOW(), 0, 1),
(12, 5, 12, 1, 1, NOW(), NOW(), 0, 1),
(13, 6, 13, 1, 1, NOW(), NOW(), 0, 1),
(14, 6, 14, 1, 1, NOW(), NOW(), 0, 1),
(15, 6, 15, 1, 1, NOW(), NOW(), 0, 1),
(16, 6, 16, 1, 1, NOW(), NOW(), 0, 1),
(17, 7, 17, 1, 1, NOW(), NOW(), 0, 1),
(18, 7, 18, 1, 1, NOW(), NOW(), 0, 1),
(19, 7, 19, 1, 1, NOW(), NOW(), 0, 1),
(20, 7, 20, 1, 1, NOW(), NOW(), 0, 1),
(21, 9, 21, 1, 1, NOW(), NOW(), 0, 1),
(22, 9, 22, 1, 1, NOW(), NOW(), 0, 1),
(23, 9, 23, 1, 1, NOW(), NOW(), 0, 1),
(24, 9, 24, 1, 1, NOW(), NOW(), 0, 1),
(25, 10, 25, 1, 1, NOW(), NOW(), 0, 1),
(26, 10, 26, 1, 1, NOW(), NOW(), 0, 1),
(27, 10, 27, 1, 1, NOW(), NOW(), 0, 1),
(28, 10, 28, 1, 1, NOW(), NOW(), 0, 1);

-- ============================================
-- 13. 字典数据
-- ============================================
INSERT INTO `sys_dict` (`id`, `name`, `code`, `description`, `sort`, `status`, `tenant_id`, `create_time`, `update_time`, `is_deleted`, `version`) VALUES
(1, '用户状态', 'user_status', '用户状态字典', 1, 1, 1, NOW(), NOW(), 0, 1),
(2, '性别', 'gender', '性别字典', 2, 1, 1, NOW(), NOW(), 0, 1),
(3, '菜单类型', 'menu_type', '菜单类型字典', 3, 1, 1, NOW(), NOW(), 0, 1),
(4, '数据权限范围', 'data_scope', '数据权限范围字典', 4, 1, 1, NOW(), NOW(), 0, 1),
(5, '角色类型', 'role_type', '角色类型字典', 5, 1, 1, NOW(), NOW(), 0, 1),
(6, '系统状态', 'system_status', '通用系统状态字典', 6, 1, 1, NOW(), NOW(), 0, 1);

INSERT INTO `sys_dict_item` (`id`, `dict_id`, `label`, `value`, `color`, `description`, `sort`, `status`, `tenant_id`, `create_time`, `update_time`, `is_deleted`, `version`) VALUES
(1, 1, '禁用', '0', 'red', NULL, 1, 1, 1, NOW(), NOW(), 0, 1),
(2, 1, '启用', '1', 'green', NULL, 2, 1, 1, NOW(), NOW(), 0, 1),
(3, 2, '未知', '0', 'default', NULL, 1, 1, 1, NOW(), NOW(), 0, 1),
(4, 2, '男', '1', 'blue', NULL, 2, 1, 1, NOW(), NOW(), 0, 1),
(5, 2, '女', '2', 'pink', NULL, 3, 1, 1, NOW(), NOW(), 0, 1),
(6, 3, '目录', '0', 'blue', NULL, 1, 1, 1, NOW(), NOW(), 0, 1),
(7, 3, '菜单', '1', 'green', NULL, 2, 1, 1, NOW(), NOW(), 0, 1),
(8, 3, '按钮', '2', 'orange', NULL, 3, 1, 1, NOW(), NOW(), 0, 1),
(9, 3, '内嵌', '3', 'purple', NULL, 4, 1, 1, NOW(), NOW(), 0, 1),
(10, 3, '外链', '4', 'cyan', NULL, 5, 1, 1, NOW(), NOW(), 0, 1),
(11, 4, '全部数据', '0', 'green', NULL, 1, 1, 1, NOW(), NOW(), 0, 1),
(12, 4, '自定义数据', '1', 'blue', NULL, 2, 1, 1, NOW(), NOW(), 0, 1),
(13, 4, '本部门及下级', '2', 'orange', NULL, 3, 1, 1, NOW(), NOW(), 0, 1),
(14, 4, '仅本部门', '3', 'cyan', NULL, 4, 1, 1, NOW(), NOW(), 0, 1),
(15, 4, '仅本人', '4', 'purple', NULL, 5, 1, 1, NOW(), NOW(), 0, 1),
(16, 5, '系统角色', '0', 'red', NULL, 1, 1, 1, NOW(), NOW(), 0, 1),
(17, 5, '业务角色', '1', 'blue', NULL, 2, 1, 1, NOW(), NOW(), 0, 1),
(18, 6, '禁用', '0', 'red', NULL, 1, 1, 1, NOW(), NOW(), 0, 1),
(19, 6, '启用', '1', 'green', NULL, 2, 1, 1, NOW(), NOW(), 0, 1);

-- ============================================
-- 14. 系统配置
-- ============================================
INSERT INTO `sys_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `group_name`, `is_system`, `status`, `sort`, `tenant_id`, `create_time`, `update_time`, `is_deleted`, `version`) VALUES
(1, 'site_name', '企业级RBAC系统', 'string', '网站名称', 'basic', 1, 1, 1, 1, NOW(), NOW(), 0, 1),
(2, 'site_description', '企业级权限管理系统', 'string', '网站描述', 'basic', 1, 1, 2, 1, NOW(), NOW(), 0, 1),
(3, 'site_keywords', 'RBAC,权限管理,企业级', 'string', '网站关键词', 'basic', 1, 1, 3, 1, NOW(), NOW(), 0, 1),
(4, 'site_icp', '京ICP备12345678号', 'string', '网站备案号', 'basic', 1, 1, 4, 1, NOW(), NOW(), 0, 1),
(5, 'enable_register', 'false', 'bool', '是否开启用户注册', 'basic', 1, 1, 5, 1, NOW(), NOW(), 0, 1),
(6, 'login_captcha', 'true', 'bool', '是否开启登录验证码', 'security', 1, 1, 1, 1, NOW(), NOW(), 0, 1),
(7, 'password_min_length', '6', 'int', '密码最小长度', 'security', 1, 1, 2, 1, NOW(), NOW(), 0, 1),
(8, 'password_max_length', '32', 'int', '密码最大长度', 'security', 1, 1, 3, 1, NOW(), NOW(), 0, 1),
(9, 'session_timeout', '1800', 'int', '会话超时时间(秒)', 'security', 1, 1, 4, 1, NOW(), NOW(), 0, 1),
(10, 'max_login_attempts', '5', 'int', '最大登录失败次数', 'security', 1, 1, 5, 1, NOW(), NOW(), 0, 1),
(11, 'upload_max_size', '10485760', 'int', '上传文件最大大小(字节)', 'file', 1, 1, 1, 1, NOW(), NOW(), 0, 1),
(12, 'upload_allow_types', 'jpg,jpeg,png,gif,pdf,doc,docx,xls,xlsx', 'string', '允许上传的文件类型', 'file', 1, 1, 2, 1, NOW(), NOW(), 0, 1);

-- ============================================
-- 15. 迁移记录
-- ============================================
INSERT INTO `sys_migration` (`version`, `name`, `description`, `type`, `status`, `executed_at`, `created_at`) VALUES
('20260411000000', 'initial_schema_v2', '初始化数据库表结构v2.0', 'schema', 2, NOW(), NOW()),
('20260411000001', 'demo_data_v2.1', '导入丰富演示数据v2.1', 'data', 2, NOW(), NOW());

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================
-- 演示数据导入完成
-- ============================================
-- 默认登录账号: admin / admin123
-- ============================================
