-- ============================================
-- 企业级RBAC系统 - 数据库表结构
-- 版本: v2.0
-- 描述: 与 SQLAlchemy 模型完全一致的表结构
-- ============================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================
-- 表: sys_user
-- ============================================
DROP TABLE IF EXISTS `sys_user`;
CREATE TABLE `sys_user` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户名',
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'BCrypt加密的密码哈希',
  `nickname` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '昵称',
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '邮箱',
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '手机号',
  `avatar` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '头像路径',
  `department_id` int DEFAULT NULL COMMENT '所属部门ID',
  `status` int DEFAULT NULL COMMENT '状态(0:禁用,1:启用)',
  `last_login_time` datetime DEFAULT NULL COMMENT '最后登录时间',
  `last_login_ip` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '最后登录IP',
  `tenant_id` int DEFAULT NULL COMMENT '租户ID',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `created_by` int DEFAULT NULL COMMENT '创建人ID',
  `updated_by` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_by` int DEFAULT NULL COMMENT '删除人ID',
  `is_deleted` int NOT NULL COMMENT '是否删除(0:未删除,1:已删除)',
  `version` int NOT NULL COMMENT '版本号(乐观锁)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_user_username` (`username`),
  KEY `ix_sys_user_phone` (`phone`),
  KEY `idx_user_department` (`department_id`),
  KEY `idx_user_email` (`email`),
  KEY `idx_user_phone` (`phone`),
  KEY `idx_user_tenant_status` (`tenant_id`,`status`),
  KEY `ix_sys_user_email` (`email`),
  KEY `idx_user_status` (`status`),
  CONSTRAINT `sys_user_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `sys_dept` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 表: sys_user_profile
-- ============================================
DROP TABLE IF EXISTS `sys_user_profile`;
CREATE TABLE `sys_user_profile` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `gender` int DEFAULT NULL COMMENT '性别(0:未知,1:男,2:女)',
  `birthday` date DEFAULT NULL COMMENT '生日',
  `id_card` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '身份证号',
  `address` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '家庭住址',
  `emergency_contact` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '紧急联系人',
  `emergency_phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '紧急联系电话',
  `position` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '职位',
  `entry_date` date DEFAULT NULL COMMENT '入职日期',
  `remark` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `tenant_id` int DEFAULT NULL COMMENT '租户ID',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `created_by` int DEFAULT NULL COMMENT '创建人ID',
  `updated_by` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_by` int DEFAULT NULL COMMENT '删除人ID',
  `is_deleted` int NOT NULL COMMENT '是否删除(0:未删除,1:已删除)',
  `version` int NOT NULL COMMENT '版本号(乐观锁)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `idx_profile_user` (`user_id`),
  CONSTRAINT `sys_user_profile_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 表: sys_role
-- ============================================
DROP TABLE IF EXISTS `sys_role`;
CREATE TABLE `sys_role` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '角色名称',
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '角色编码',
  `parent_id` int DEFAULT NULL COMMENT '父角色ID',
  `level` int DEFAULT NULL COMMENT '角色层级',
  `type` int DEFAULT NULL COMMENT '角色类型(0:系统角色, 1:功能角色, 2:数据角色, 3:自定义角色)',
  `data_scope` int DEFAULT NULL COMMENT '数据范围(0:全部,1:本部门,2:本部门及下级,3:仅本人,4:自定义)',
  `sort` int DEFAULT NULL COMMENT '排序',
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '角色描述',
  `status` int DEFAULT NULL COMMENT '状态(0:禁用,1:启用)',
  `tenant_id` int DEFAULT NULL COMMENT '租户ID',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `created_by` int DEFAULT NULL COMMENT '创建人ID',
  `updated_by` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_by` int DEFAULT NULL COMMENT '删除人ID',
  `is_deleted` int NOT NULL COMMENT '是否删除(0:未删除,1:已删除)',
  `version` int NOT NULL COMMENT '版本号(乐观锁)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `code` (`code`),
  KEY `idx_role_status` (`status`),
  KEY `idx_role_parent` (`parent_id`),
  KEY `idx_role_tenant_status` (`tenant_id`,`status`),
  KEY `idx_role_type` (`type`),
  CONSTRAINT `sys_role_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `sys_role` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 表: sys_permission
-- ============================================
DROP TABLE IF EXISTS `sys_permission`;
CREATE TABLE `sys_permission` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '权限名称',
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '权限编码',
  `type` int NOT NULL COMMENT '权限类型(0:菜单, 1:按钮, 2:API, 3:数据, 4:字段)',
  `resource_type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '资源类型',
  `resource_id` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '资源ID',
  `action` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '操作类型(view, create, update, delete, export)',
  `path` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '访问路径(API路径或菜单路径)',
  `method` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '请求方法(GET, POST, PUT, DELETE等)',
  `parent_id` int DEFAULT NULL COMMENT '父权限ID',
  `level` int DEFAULT NULL COMMENT '权限层级',
  `status` int DEFAULT NULL COMMENT '状态(0:禁用,1:启用)',
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '权限描述',
  `tenant_id` int DEFAULT NULL COMMENT '租户ID',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `created_by` int DEFAULT NULL COMMENT '创建人ID',
  `updated_by` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_by` int DEFAULT NULL COMMENT '删除人ID',
  `is_deleted` int NOT NULL COMMENT '是否删除(0:未删除,1:已删除)',
  `version` int NOT NULL COMMENT '版本号(乐观锁)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `parent_id` (`parent_id`),
  KEY `idx_permission_status` (`status`),
  KEY `idx_permission_type` (`type`),
  KEY `idx_perm_tenant_status` (`tenant_id`,`status`),
  CONSTRAINT `sys_permission_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `sys_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 表: sys_dept
-- ============================================
DROP TABLE IF EXISTS `sys_dept`;
CREATE TABLE `sys_dept` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '部门名称',
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '部门编码',
  `parent_id` int DEFAULT NULL COMMENT '父部门ID',
  `leader_id` int DEFAULT NULL COMMENT '部门负责人ID',
  `level` int DEFAULT NULL COMMENT '部门层级',
  `path` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '部门路径，用逗号分隔的ID，如：1,2,3',
  `contact_phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '联系电话',
  `address` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '部门地址',
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '部门描述',
  `status` int DEFAULT NULL COMMENT '状态(0:禁用,1:启用)',
  `tenant_id` int DEFAULT NULL COMMENT '租户ID',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `created_by` int DEFAULT NULL COMMENT '创建人ID',
  `updated_by` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_by` int DEFAULT NULL COMMENT '删除人ID',
  `is_deleted` int NOT NULL COMMENT '是否删除(0:未删除,1:已删除)',
  `version` int NOT NULL COMMENT '版本号(乐观锁)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `idx_department_leader` (`leader_id`),
  KEY `idx_dept_path` (`path`),
  KEY `idx_dept_tenant_status` (`tenant_id`,`status`),
  KEY `idx_department_parent` (`parent_id`),
  CONSTRAINT `sys_dept_ibfk_1` FOREIGN KEY (`leader_id`) REFERENCES `sys_user` (`id`),
  CONSTRAINT `sys_dept_ibfk_2` FOREIGN KEY (`parent_id`) REFERENCES `sys_dept` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 表: sys_menu
-- ============================================
DROP TABLE IF EXISTS `sys_menu`;
CREATE TABLE `sys_menu` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '菜单名称',
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '菜单编码',
  `parent_id` int DEFAULT NULL COMMENT '父菜单ID',
  `level` int DEFAULT NULL COMMENT '菜单层级',
  `type` int NOT NULL COMMENT '菜单类型(0:目录,1:菜单,2:按钮,3:内嵌,4:外链)',
  `path` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '访问路径',
  `component` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '组件路径',
  `icon` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '菜单图标',
  `sort` int DEFAULT NULL COMMENT '排序',
  `status` int DEFAULT NULL COMMENT '状态(0:禁用,1:启用)',
  `tenant_id` int DEFAULT NULL COMMENT '租户ID',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `created_by` int DEFAULT NULL COMMENT '创建人ID',
  `updated_by` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_by` int DEFAULT NULL COMMENT '删除人ID',
  `is_deleted` int NOT NULL COMMENT '是否删除(0:未删除,1:已删除)',
  `version` int NOT NULL COMMENT '版本号(乐观锁)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `idx_menu_parent` (`parent_id`),
  KEY `idx_menu_tenant_status` (`tenant_id`,`status`),
  KEY `idx_menu_sort` (`sort`),
  CONSTRAINT `sys_menu_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `sys_menu` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 表: sys_user_role
-- ============================================
DROP TABLE IF EXISTS `sys_user_role`;
CREATE TABLE `sys_user_role` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `role_id` int NOT NULL COMMENT '角色ID',
  `is_primary` tinyint(1) DEFAULT NULL COMMENT '是否主角色',
  `effective_time` datetime DEFAULT NULL COMMENT '生效时间',
  `expire_time` datetime DEFAULT NULL COMMENT '过期时间',
  `status` int DEFAULT NULL COMMENT '状态(0:禁用,1:启用)',
  `tenant_id` int DEFAULT NULL COMMENT '租户ID',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `created_by` int DEFAULT NULL COMMENT '创建人ID',
  `updated_by` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_by` int DEFAULT NULL COMMENT '删除人ID',
  `is_deleted` int NOT NULL COMMENT '是否删除(0:未删除,1:已删除)',
  `version` int NOT NULL COMMENT '版本号(乐观锁)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_role` (`user_id`,`role_id`),
  KEY `idx_user_role_role` (`role_id`),
  KEY `idx_user_role_user` (`user_id`),
  CONSTRAINT `sys_user_role_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`),
  CONSTRAINT `sys_user_role_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `sys_role` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 表: sys_role_permission
-- ============================================
DROP TABLE IF EXISTS `sys_role_permission`;
CREATE TABLE `sys_role_permission` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `role_id` int NOT NULL COMMENT '角色ID',
  `permission_id` int NOT NULL COMMENT '权限ID',
  `status` int DEFAULT NULL COMMENT '状态(0:禁用,1:启用)',
  `tenant_id` int DEFAULT NULL COMMENT '租户ID',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `created_by` int DEFAULT NULL COMMENT '创建人ID',
  `updated_by` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_by` int DEFAULT NULL COMMENT '删除人ID',
  `is_deleted` int NOT NULL COMMENT '是否删除(0:未删除,1:已删除)',
  `version` int NOT NULL COMMENT '版本号(乐观锁)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_role_permission` (`role_id`,`permission_id`),
  KEY `idx_role_permission_role` (`role_id`),
  KEY `idx_role_permission_permission` (`permission_id`),
  CONSTRAINT `sys_role_permission_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `sys_role` (`id`),
  CONSTRAINT `sys_role_permission_ibfk_2` FOREIGN KEY (`permission_id`) REFERENCES `sys_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 表: sys_menu_permission
-- ============================================
DROP TABLE IF EXISTS `sys_menu_permission`;
CREATE TABLE `sys_menu_permission` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `menu_id` int NOT NULL COMMENT '菜单ID',
  `permission_id` int NOT NULL COMMENT '权限ID',
  `status` int DEFAULT NULL COMMENT '状态(0:禁用,1:启用)',
  `tenant_id` int DEFAULT NULL COMMENT '租户ID',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `created_by` int DEFAULT NULL COMMENT '创建人ID',
  `updated_by` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_by` int DEFAULT NULL COMMENT '删除人ID',
  `is_deleted` int NOT NULL COMMENT '是否删除(0:未删除,1:已删除)',
  `version` int NOT NULL COMMENT '版本号(乐观锁)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_menu_permission` (`menu_id`,`permission_id`),
  KEY `idx_menu_perm_permission` (`permission_id`),
  KEY `idx_menu_perm_menu` (`menu_id`),
  CONSTRAINT `sys_menu_permission_ibfk_1` FOREIGN KEY (`menu_id`) REFERENCES `sys_menu` (`id`),
  CONSTRAINT `sys_menu_permission_ibfk_2` FOREIGN KEY (`permission_id`) REFERENCES `sys_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 表: sys_user_group
-- ============================================
DROP TABLE IF EXISTS `sys_user_group`;
CREATE TABLE `sys_user_group` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户组名称',
  `code` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户组编码',
  `description` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '描述',
  `status` int DEFAULT NULL COMMENT '状态(0:禁用,1:启用)',
  `sort` int DEFAULT NULL COMMENT '排序',
  `tenant_id` int DEFAULT NULL COMMENT '租户ID',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `created_by` int DEFAULT NULL COMMENT '创建人ID',
  `updated_by` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_by` int DEFAULT NULL COMMENT '删除人ID',
  `is_deleted` int NOT NULL COMMENT '是否删除(0:未删除,1:已删除)',
  `version` int NOT NULL COMMENT '版本号(乐观锁)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_user_group_code` (`code`),
  KEY `idx_user_group_code` (`code`),
  KEY `idx_ug_tenant_status` (`tenant_id`,`status`),
  KEY `idx_user_group_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 表: sys_user_group_relation
-- ============================================
DROP TABLE IF EXISTS `sys_user_group_relation`;
CREATE TABLE `sys_user_group_relation` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `user_group_id` int NOT NULL COMMENT '用户组ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `status` int DEFAULT NULL COMMENT '状态(0:禁用,1:启用)',
  `tenant_id` int DEFAULT NULL COMMENT '租户ID',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `created_by` int DEFAULT NULL COMMENT '创建人ID',
  `updated_by` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_by` int DEFAULT NULL COMMENT '删除人ID',
  `is_deleted` int NOT NULL COMMENT '是否删除(0:未删除,1:已删除)',
  `version` int NOT NULL COMMENT '版本号(乐观锁)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_group_user` (`user_group_id`,`user_id`),
  KEY `idx_ugr_user` (`user_id`),
  KEY `idx_ugr_user_group` (`user_group_id`),
  CONSTRAINT `sys_user_group_relation_ibfk_1` FOREIGN KEY (`user_group_id`) REFERENCES `sys_user_group` (`id`),
  CONSTRAINT `sys_user_group_relation_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 表: sys_user_group_role_relation
-- ============================================
DROP TABLE IF EXISTS `sys_user_group_role_relation`;
CREATE TABLE `sys_user_group_role_relation` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `user_group_id` int NOT NULL COMMENT '用户组ID',
  `role_id` int NOT NULL COMMENT '角色ID',
  `status` int DEFAULT NULL COMMENT '状态(0:禁用,1:启用)',
  `tenant_id` int DEFAULT NULL COMMENT '租户ID',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `created_by` int DEFAULT NULL COMMENT '创建人ID',
  `updated_by` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_by` int DEFAULT NULL COMMENT '删除人ID',
  `is_deleted` int NOT NULL COMMENT '是否删除(0:未删除,1:已删除)',
  `version` int NOT NULL COMMENT '版本号(乐观锁)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_group_role` (`user_group_id`,`role_id`),
  KEY `idx_ugrr_user_group` (`user_group_id`),
  KEY `idx_ugrr_role` (`role_id`),
  CONSTRAINT `sys_user_group_role_relation_ibfk_1` FOREIGN KEY (`user_group_id`) REFERENCES `sys_user_group` (`id`),
  CONSTRAINT `sys_user_group_role_relation_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `sys_role` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 表: sys_dict
-- ============================================
DROP TABLE IF EXISTS `sys_dict`;
CREATE TABLE `sys_dict` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '字典名称',
  `code` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '字典编码',
  `description` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '描述',
  `status` int DEFAULT NULL COMMENT '状态(0:禁用,1:启用)',
  `sort` int DEFAULT NULL COMMENT '排序',
  `tenant_id` int DEFAULT NULL COMMENT '租户ID',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `created_by` int DEFAULT NULL COMMENT '创建人ID',
  `updated_by` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_by` int DEFAULT NULL COMMENT '删除人ID',
  `is_deleted` int NOT NULL COMMENT '是否删除(0:未删除,1:已删除)',
  `version` int NOT NULL COMMENT '版本号(乐观锁)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_dict_code` (`code`),
  KEY `idx_dict_code` (`code`),
  KEY `idx_dict_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 表: sys_dict_item
-- ============================================
DROP TABLE IF EXISTS `sys_dict_item`;
CREATE TABLE `sys_dict_item` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `dict_id` int NOT NULL COMMENT '字典ID',
  `label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '标签',
  `value` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '值',
  `color` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '颜色',
  `description` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '描述',
  `status` int DEFAULT NULL COMMENT '状态(0:禁用,1:启用)',
  `sort` int DEFAULT NULL COMMENT '排序',
  `tenant_id` int DEFAULT NULL COMMENT '租户ID',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `created_by` int DEFAULT NULL COMMENT '创建人ID',
  `updated_by` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_by` int DEFAULT NULL COMMENT '删除人ID',
  `is_deleted` int NOT NULL COMMENT '是否删除(0:未删除,1:已删除)',
  `version` int NOT NULL COMMENT '版本号(乐观锁)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_dict_value` (`dict_id`,`value`),
  KEY `idx_dict_item_status` (`status`),
  KEY `idx_dict_item_dict` (`dict_id`),
  CONSTRAINT `sys_dict_item_ibfk_1` FOREIGN KEY (`dict_id`) REFERENCES `sys_dict` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 表: sys_config
-- ============================================
DROP TABLE IF EXISTS `sys_config`;
CREATE TABLE `sys_config` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `config_key` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '配置键',
  `config_value` text COLLATE utf8mb4_unicode_ci COMMENT '配置值',
  `config_type` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '配置类型(string,int,bool,json)',
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '配置描述',
  `group_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '配置分组',
  `is_system` int DEFAULT NULL COMMENT '是否系统配置(0:否,1:是)',
  `status` int DEFAULT NULL COMMENT '状态(0:禁用,1:启用)',
  `sort` int DEFAULT NULL COMMENT '排序',
  `tenant_id` int DEFAULT NULL COMMENT '租户ID',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `created_by` int DEFAULT NULL COMMENT '创建人ID',
  `updated_by` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_by` int DEFAULT NULL COMMENT '删除人ID',
  `is_deleted` int NOT NULL COMMENT '是否删除(0:未删除,1:已删除)',
  `version` int NOT NULL COMMENT '版本号(乐观锁)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_config_config_key` (`config_key`),
  KEY `idx_config_group` (`group_name`),
  KEY `idx_config_status` (`status`),
  KEY `idx_config_key` (`config_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 表: sys_operation_log
-- ============================================
DROP TABLE IF EXISTS `sys_operation_log`;
CREATE TABLE `sys_operation_log` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `user_id` int DEFAULT NULL COMMENT '操作用户ID',
  `username` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '操作用户名',
  `module` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模块',
  `operation` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '操作类型',
  `description` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '操作描述',
  `request_method` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '请求方法',
  `request_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '请求URL',
  `request_params` text COLLATE utf8mb4_unicode_ci COMMENT '请求参数',
  `response_result` text COLLATE utf8mb4_unicode_ci COMMENT '响应结果',
  `execution_time` int DEFAULT NULL COMMENT '执行时长(毫秒)',
  `ip_address` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'IP地址',
  `user_agent` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户代理',
  `status` int DEFAULT NULL COMMENT '状态(0:失败,1:成功)',
  `error_message` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '错误信息',
  `tenant_id` int DEFAULT NULL COMMENT '租户ID',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `created_by` int DEFAULT NULL COMMENT '创建人ID',
  `updated_by` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_by` int DEFAULT NULL COMMENT '删除人ID',
  `is_deleted` int NOT NULL COMMENT '是否删除(0:未删除,1:已删除)',
  `version` int NOT NULL COMMENT '版本号(乐观锁)',
  PRIMARY KEY (`id`),
  KEY `idx_op_log_user` (`user_id`),
  KEY `idx_op_log_status` (`status`),
  KEY `idx_op_log_create_time` (`create_time`),
  KEY `idx_op_log_module` (`module`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 表: sys_audit_log
-- ============================================
DROP TABLE IF EXISTS `sys_audit_log`;
CREATE TABLE `sys_audit_log` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `table_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '表名',
  `record_id` int NOT NULL COMMENT '记录ID',
  `operation_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '操作类型(INSERT/UPDATE/DELETE)',
  `field_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '字段名',
  `old_value` text COLLATE utf8mb4_unicode_ci COMMENT '旧值',
  `new_value` text COLLATE utf8mb4_unicode_ci COMMENT '新值',
  `user_id` int DEFAULT NULL COMMENT '操作用户ID',
  `username` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '操作用户名',
  `change_reason` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '变更原因',
  `tenant_id` int DEFAULT NULL COMMENT '租户ID',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `created_by` int DEFAULT NULL COMMENT '创建人ID',
  `updated_by` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_by` int DEFAULT NULL COMMENT '删除人ID',
  `is_deleted` int NOT NULL COMMENT '是否删除(0:未删除,1:已删除)',
  `version` int NOT NULL COMMENT '版本号(乐观锁)',
  PRIMARY KEY (`id`),
  KEY `idx_audit_record` (`table_name`,`record_id`),
  KEY `idx_audit_create_time` (`create_time`),
  KEY `idx_audit_table` (`table_name`),
  KEY `idx_audit_operation` (`operation_type`),
  KEY `idx_audit_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 表: sys_user_session
-- ============================================
DROP TABLE IF EXISTS `sys_user_session`;
CREATE TABLE `sys_user_session` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `session_id` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '会话ID',
  `access_token` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '访问令牌',
  `refresh_token` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '刷新令牌',
  `device_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '设备类型',
  `device_info` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '设备信息',
  `ip_address` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'IP地址',
  `login_time` datetime NOT NULL COMMENT '登录时间',
  `last_active_time` datetime NOT NULL COMMENT '最后活跃时间',
  `expire_time` datetime NOT NULL COMMENT '过期时间',
  `status` int DEFAULT NULL COMMENT '状态(0:已失效,1:有效)',
  `tenant_id` int DEFAULT NULL COMMENT '租户ID',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `created_by` int DEFAULT NULL COMMENT '创建人ID',
  `updated_by` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_by` int DEFAULT NULL COMMENT '删除人ID',
  `is_deleted` int NOT NULL COMMENT '是否删除(0:未删除,1:已删除)',
  `version` int NOT NULL COMMENT '版本号(乐观锁)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_user_session_session_id` (`session_id`),
  KEY `idx_session_expire` (`expire_time`),
  KEY `idx_session_status` (`status`),
  KEY `idx_session_user` (`user_id`),
  CONSTRAINT `sys_user_session_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 表: sys_data_permission_rule
-- ============================================
DROP TABLE IF EXISTS `sys_data_permission_rule`;
CREATE TABLE `sys_data_permission_rule` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '规则名称',
  `code` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '规则编码',
  `permission_id` int NOT NULL COMMENT '关联权限ID',
  `resource_table` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '资源表名',
  `rule_type` int NOT NULL COMMENT '规则类型(0:全部,1:本部门,2:本部门及下级,3:仅本人,4:自定义)',
  `rule_expression` text COLLATE utf8mb4_unicode_ci COMMENT '自定义规则表达式(SQL WHERE片段)',
  `status` int DEFAULT NULL COMMENT '状态(0:禁用,1:启用)',
  `description` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '规则描述',
  `tenant_id` int DEFAULT NULL COMMENT '租户ID',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `created_by` int DEFAULT NULL COMMENT '创建人ID',
  `updated_by` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_by` int DEFAULT NULL COMMENT '删除人ID',
  `is_deleted` int NOT NULL COMMENT '是否删除(0:未删除,1:已删除)',
  `version` int NOT NULL COMMENT '版本号(乐观锁)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `idx_data_perm_permission` (`permission_id`),
  KEY `idx_data_perm_status` (`status`),
  CONSTRAINT `sys_data_permission_rule_ibfk_1` FOREIGN KEY (`permission_id`) REFERENCES `sys_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 表: sys_migration
-- ============================================
DROP TABLE IF EXISTS `sys_migration`;
CREATE TABLE `sys_migration` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `version` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '版本号',
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '迁移名称',
  `description` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '描述',
  `type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'schema' COMMENT '类型:schema/data',
  `status` tinyint NOT NULL DEFAULT '1' COMMENT '状态:0待执行,1执行中,2成功,3失败',
  `error_msg` text COLLATE utf8mb4_unicode_ci COMMENT '错误信息',
  `executed_at` datetime DEFAULT NULL COMMENT '执行时间',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_version` (`version`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='迁移记录表';

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================
-- 表结构导出完成
-- ============================================