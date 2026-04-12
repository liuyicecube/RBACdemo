# 企业级RBAC系统 - 数据库结构文档

## 概述

本文档描述了企业级RBAC（基于角色的访问控制）系统的数据库结构设计。该系统包含完整的用户管理、角色管理、权限管理、部门管理、菜单管理、用户组管理、审计日志等功能。

**数据库版本**: 1.0.0  
**字符集**: utf8mb4  
**排序规则**: utf8mb4_unicode_ci  
**数据库引擎**: InnoDB

---

## 数据库表清单

| 序号 | 表名 | 中文名称 | 说明 |
|------|------|----------|------|
| 1 | sys_user | 用户表 | 存储系统用户基本信息 |
| 2 | sys_user_profile | 用户扩展信息表 | 存储用户的扩展信息 |
| 3 | sys_role | 角色表 | 存储系统角色信息 |
| 4 | sys_user_role | 用户角色关联表 | 用户与角色的多对多关系 |
| 5 | sys_permission | 权限表 | 存储系统权限信息 |
| 6 | sys_role_permission | 角色权限关联表 | 角色与权限的多对多关系 |
| 7 | sys_dept | 部门表 | 存储组织部门信息 |
| 8 | sys_menu | 菜单表 | 存储系统菜单信息 |
| 9 | sys_menu_permission | 菜单权限关联表 | 菜单与权限的关联关系 |
| 10 | sys_user_group | 用户组表 | 存储用户组信息 |
| 11 | sys_user_group_relation | 用户组-用户关联表 | 用户组与用户的多对多关系 |
| 12 | sys_user_group_role_relation | 用户组-角色关联表 | 用户组与角色的多对多关系 |
| 13 | sys_user_session | 用户会话表 | 存储用户登录会话信息 |
| 14 | sys_audit_log | 审计日志表 | 记录数据变更的审计日志 |
| 15 | sys_operation_log | 操作日志表 | 记录用户操作日志 |
| 16 | sys_config | 系统配置表 | 存储系统配置信息 |
| 17 | sys_dict | 系统字典表 | 存储系统字典类型 |
| 18 | sys_dict_item | 系统字典项表 | 存储字典项数据 |
| 19 | sys_data_permission_rule | 数据权限规则表 | 存储数据权限规则 |

---

## 基础模型字段说明

所有表都继承自基础模型，包含以下公共字段：

| 字段名 | 类型 | 允许NULL | 默认值 | 说明 |
|--------|------|----------|--------|------|
| tenant_id | int(11) | YES | NULL | 租户ID（支持多租户） |
| create_time | datetime | NO | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | CURRENT_TIMESTAMP ON UPDATE | 更新时间 |
| delete_time | datetime | YES | NULL | 删除时间（软删除） |
| created_by | int(11) | YES | NULL | 创建人ID |
| updated_by | int(11) | YES | NULL | 更新人ID |
| deleted_by | int(11) | YES | NULL | 删除人ID |
| is_deleted | int(11) | NO | 0 | 是否删除（0:未删除, 1:已删除） |
| version | int(11) | NO | 1 | 版本号（乐观锁） |

---

## 表结构详细说明

### 1. 用户表 (sys_user)

存储系统用户的基本信息。

| 字段名 | 类型 | 允许NULL | 默认值 | 说明 |
|--------|------|----------|--------|------|
| id | int(11) | NO | AUTO_INCREMENT | 主键ID |
| username | varchar(50) | NO | | 用户名（唯一） |
| password | varchar(255) | NO | | BCrypt加密的密码哈希 |
| nickname | varchar(50) | NO | | 昵称 |
| email | varchar(100) | YES | NULL | 邮箱 |
| phone | varchar(20) | YES | NULL | 手机号 |
| avatar | varchar(255) | YES | NULL | 头像路径 |
| department_id | int(11) | YES | NULL | 所属部门ID（外键） |
| status | int(11) | YES | 1 | 状态（0:禁用, 1:启用） |
| last_login_time | datetime | YES | NULL | 最后登录时间 |
| last_login_ip | varchar(50) | YES | NULL | 最后登录IP |

**索引**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_username` (`username`)
- INDEX `idx_user_status` (`status`)
- INDEX `idx_user_department` (`department_id`)
- INDEX `idx_user_email` (`email`)
- INDEX `idx_user_phone` (`phone`)

---

### 2. 用户扩展信息表 (sys_user_profile)

存储用户的详细扩展信息。

| 字段名 | 类型 | 允许NULL | 默认值 | 说明 |
|--------|------|----------|--------|------|
| id | int(11) | NO | AUTO_INCREMENT | 主键ID |
| user_id | int(11) | NO | | 用户ID（外键，唯一） |
| gender | int(11) | YES | NULL | 性别（0:未知, 1:男, 2:女） |
| birthday | date | YES | NULL | 生日 |
| id_card | varchar(20) | YES | NULL | 身份证号 |
| address | varchar(255) | YES | NULL | 家庭住址 |
| emergency_contact | varchar(50) | YES | NULL | 紧急联系人 |
| emergency_phone | varchar(20) | YES | NULL | 紧急联系电话 |
| position | varchar(50) | YES | NULL | 职位 |
| entry_date | date | YES | NULL | 入职日期 |
| remark | text | YES | NULL | 备注 |

**索引**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_user_id` (`user_id`)

---

### 3. 角色表 (sys_role)

存储系统角色信息，支持角色层级结构。

| 字段名 | 类型 | 允许NULL | 默认值 | 说明 |
|--------|------|----------|--------|------|
| id | int(11) | NO | AUTO_INCREMENT | 主键ID |
| name | varchar(50) | NO | | 角色名称（唯一） |
| code | varchar(50) | NO | | 角色编码（唯一） |
| parent_id | int(11) | YES | NULL | 父角色ID（外键） |
| level | int(11) | YES | 1 | 角色层级 |
| type | int(11) | YES | 3 | 角色类型（0:系统角色, 1:功能角色, 2:数据角色, 3:自定义角色） |
| data_scope | int(11) | YES | 0 | 数据范围（0:全部, 1:本部门, 2:本部门及下级, 3:仅本人, 4:自定义） |
| sort | int(11) | YES | 0 | 排序 |
| description | varchar(255) | YES | NULL | 角色描述 |
| status | int(11) | YES | 1 | 状态（0:禁用, 1:启用） |

**索引**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_name` (`name`)
- UNIQUE KEY `uk_code` (`code`)
- INDEX `idx_role_status` (`status`)
- INDEX `idx_role_parent` (`parent_id`)
- INDEX `idx_role_type` (`type`)

---

### 4. 用户角色关联表 (sys_user_role)

用户与角色的多对多关联表。

| 字段名 | 类型 | 允许NULL | 默认值 | 说明 |
|--------|------|----------|--------|------|
| id | int(11) | NO | AUTO_INCREMENT | 主键ID |
| user_id | int(11) | NO | | 用户ID（外键） |
| role_id | int(11) | NO | | 角色ID（外键） |
| is_primary | tinyint(1) | YES | 0 | 是否主角色 |
| effective_time | datetime | YES | NULL | 生效时间 |
| expire_time | datetime | YES | NULL | 过期时间 |
| status | int(11) | YES | 1 | 状态（0:禁用, 1:启用） |

**索引**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_user_role` (`user_id`, `role_id`)
- INDEX `idx_user_role_user` (`user_id`)
- INDEX `idx_user_role_role` (`role_id`)

---

### 5. 权限表 (sys_permission)

存储系统权限信息，支持权限层级结构。

| 字段名 | 类型 | 允许NULL | 默认值 | 说明 |
|--------|------|----------|--------|------|
| id | int(11) | NO | AUTO_INCREMENT | 主键ID |
| name | varchar(50) | NO | | 权限名称 |
| code | varchar(50) | NO | | 权限编码（唯一） |
| type | int(11) | NO | | 权限类型（0:菜单, 1:按钮, 2:API, 3:数据, 4:字段） |
| resource_type | varchar(50) | NO | | 资源类型 |
| resource_id | varchar(100) | YES | NULL | 资源ID |
| action | varchar(20) | NO | | 操作类型（view, create, update, delete, export） |
| path | varchar(255) | YES | NULL | 访问路径（API路径或菜单路径） |
| method | varchar(10) | YES | NULL | 请求方法（GET, POST, PUT, DELETE等） |
| parent_id | int(11) | YES | NULL | 父权限ID（外键） |
| level | int(11) | YES | 1 | 权限层级 |
| status | int(11) | YES | 1 | 状态（0:禁用, 1:启用） |
| description | varchar(255) | YES | NULL | 权限描述 |

**索引**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_code` (`code`)
- INDEX `idx_permission_type` (`type`)
- INDEX `idx_permission_status` (`status`)

---

### 6. 角色权限关联表 (sys_role_permission)

角色与权限的多对多关联表。

| 字段名 | 类型 | 允许NULL | 默认值 | 说明 |
|--------|------|----------|--------|------|
| id | int(11) | NO | AUTO_INCREMENT | 主键ID |
| role_id | int(11) | NO | | 角色ID（外键） |
| permission_id | int(11) | NO | | 权限ID（外键） |
| status | int(11) | YES | 1 | 状态（0:禁用, 1:启用） |

**索引**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_role_permission` (`role_id`, `permission_id`)
- INDEX `idx_role_permission_role` (`role_id`)
- INDEX `idx_role_permission_permission` (`permission_id`)

---

### 7. 部门表 (sys_dept)

存储组织部门信息，支持部门层级结构。

| 字段名 | 类型 | 允许NULL | 默认值 | 说明 |
|--------|------|----------|--------|------|
| id | int(11) | NO | AUTO_INCREMENT | 主键ID |
| name | varchar(50) | NO | | 部门名称 |
| code | varchar(50) | NO | | 部门编码（唯一） |
| parent_id | int(11) | YES | NULL | 父部门ID（外键） |
| leader_id | int(11) | YES | NULL | 部门负责人ID（外键） |
| level | int(11) | YES | 1 | 部门层级 |
| path | varchar(500) | YES | NULL | 部门路径（用逗号分隔的ID，如：1,2,3） |
| contact_phone | varchar(20) | YES | NULL | 联系电话 |
| address | varchar(255) | YES | NULL | 部门地址 |
| description | varchar(255) | YES | NULL | 部门描述 |
| status | int(11) | YES | 1 | 状态（0:禁用, 1:启用） |

**索引**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_code` (`code`)
- INDEX `idx_department_parent` (`parent_id`)
- INDEX `idx_department_leader` (`leader_id`)
- INDEX `idx_dept_path` (`path`)

---

### 8. 菜单表 (sys_menu)

存储系统菜单信息，支持菜单层级结构。

| 字段名 | 类型 | 允许NULL | 默认值 | 说明 |
|--------|------|----------|--------|------|
| id | int(11) | NO | AUTO_INCREMENT | 主键ID |
| name | varchar(50) | NO | | 菜单名称 |
| code | varchar(50) | NO | | 菜单编码（唯一） |
| parent_id | int(11) | YES | NULL | 父菜单ID（外键） |
| level | int(11) | YES | 1 | 菜单层级 |
| type | int(11) | NO | | 菜单类型（0:目录, 1:菜单, 2:按钮, 3:内嵌, 4:外链） |
| path | varchar(255) | YES | NULL | 访问路径 |
| component | varchar(255) | YES | NULL | 组件路径 |
| icon | varchar(50) | YES | NULL | 菜单图标 |
| sort | int(11) | YES | 0 | 排序 |
| status | int(11) | YES | 1 | 状态（0:禁用, 1:启用） |

**索引**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_code` (`code`)
- INDEX `idx_menu_parent` (`parent_id`)
- INDEX `idx_menu_sort` (`sort`)

---

### 9. 菜单权限关联表 (sys_menu_permission)

菜单与权限的关联表。

| 字段名 | 类型 | 允许NULL | 默认值 | 说明 |
|--------|------|----------|--------|------|
| id | int(11) | NO | AUTO_INCREMENT | 主键ID |
| menu_id | int(11) | NO | | 菜单ID（外键） |
| permission_id | int(11) | NO | | 权限ID（外键） |
| status | int(11) | YES | 1 | 状态（0:禁用, 1:启用） |

**索引**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_menu_permission` (`menu_id`, `permission_id`)
- INDEX `idx_menu_perm_menu` (`menu_id`)
- INDEX `idx_menu_perm_permission` (`permission_id`)

---

### 10. 用户组表 (sys_user_group)

存储用户组信息。

| 字段名 | 类型 | 允许NULL | 默认值 | 说明 |
|--------|------|----------|--------|------|
| id | int(11) | NO | AUTO_INCREMENT | 主键ID |
| name | varchar(100) | NO | | 用户组名称 |
| code | varchar(100) | NO | | 用户组编码（唯一） |
| description | varchar(500) | YES | NULL | 描述 |
| status | int(11) | YES | 1 | 状态（0:禁用, 1:启用） |
| sort | int(11) | YES | 0 | 排序 |

**索引**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_code` (`code`)
- INDEX `idx_user_group_status` (`status`)
- INDEX `idx_user_group_code` (`code`)

---

### 11. 用户组-用户关联表 (sys_user_group_relation)

用户组与用户的多对多关联表。

| 字段名 | 类型 | 允许NULL | 默认值 | 说明 |
|--------|------|----------|--------|------|
| id | int(11) | NO | AUTO_INCREMENT | 主键ID |
| user_group_id | int(11) | NO | | 用户组ID（外键） |
| user_id | int(11) | NO | | 用户ID（外键） |
| status | int(11) | YES | 1 | 状态（0:禁用, 1:启用） |

**索引**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_user_group_user` (`user_group_id`, `user_id`)
- INDEX `idx_ugr_user_group` (`user_group_id`)
- INDEX `idx_ugr_user` (`user_id`)

---

### 12. 用户组-角色关联表 (sys_user_group_role_relation)

用户组与角色的多对多关联表。

| 字段名 | 类型 | 允许NULL | 默认值 | 说明 |
|--------|------|----------|--------|------|
| id | int(11) | NO | AUTO_INCREMENT | 主键ID |
| user_group_id | int(11) | NO | | 用户组ID（外键） |
| role_id | int(11) | NO | | 角色ID（外键） |
| status | int(11) | YES | 1 | 状态（0:禁用, 1:启用） |

**索引**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_user_group_role` (`user_group_id`, `role_id`)
- INDEX `idx_ugrr_user_group` (`user_group_id`)
- INDEX `idx_ugrr_role` (`role_id`)

---

### 13. 用户会话表 (sys_user_session)

存储用户登录会话信息。

| 字段名 | 类型 | 允许NULL | 默认值 | 说明 |
|--------|------|----------|--------|------|
| id | int(11) | NO | AUTO_INCREMENT | 主键ID |
| user_id | int(11) | NO | | 用户ID（外键） |
| session_id | varchar(100) | NO | | 会话ID（唯一） |
| access_token | varchar(500) | NO | | 访问令牌 |
| refresh_token | varchar(500) | YES | NULL | 刷新令牌 |
| device_type | varchar(50) | YES | NULL | 设备类型 |
| device_info | varchar(500) | YES | NULL | 设备信息 |
| ip_address | varchar(50) | YES | NULL | IP地址 |
| login_time | datetime | NO | | 登录时间 |
| last_active_time | datetime | NO | | 最后活跃时间 |
| expire_time | datetime | NO | | 过期时间 |
| status | int(11) | YES | 1 | 状态（0:已失效, 1:有效） |

**索引**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_session_id` (`session_id`)
- INDEX `idx_session_user` (`user_id`)
- INDEX `idx_session_status` (`status`)
- INDEX `idx_session_expire` (`expire_time`)

---

### 14. 审计日志表 (sys_audit_log)

记录数据变更的审计日志。

| 字段名 | 类型 | 允许NULL | 默认值 | 说明 |
|--------|------|----------|--------|------|
| id | int(11) | NO | AUTO_INCREMENT | 主键ID |
| table_name | varchar(100) | NO | | 表名 |
| record_id | int(11) | NO | | 记录ID |
| operation_type | varchar(20) | NO | | 操作类型（INSERT/UPDATE/DELETE） |
| field_name | varchar(100) | YES | NULL | 字段名 |
| old_value | text | YES | NULL | 旧值 |
| new_value | text | YES | NULL | 新值 |
| user_id | int(11) | YES | NULL | 操作用户ID |
| username | varchar(50) | YES | NULL | 操作用户名 |
| change_reason | varchar(500) | YES | NULL | 变更原因 |

**索引**:
- PRIMARY KEY (`id`)
- INDEX `idx_audit_table` (`table_name`)
- INDEX `idx_audit_record` (`table_name`, `record_id`)
- INDEX `idx_audit_operation` (`operation_type`)
- INDEX `idx_audit_user` (`user_id`)

---

### 15. 操作日志表 (sys_operation_log)

记录用户操作日志。

| 字段名 | 类型 | 允许NULL | 默认值 | 说明 |
|--------|------|----------|--------|------|
| id | int(11) | NO | AUTO_INCREMENT | 主键ID |
| user_id | int(11) | YES | NULL | 操作用户ID |
| username | varchar(50) | YES | NULL | 操作用户名 |
| module | varchar(50) | NO | | 模块 |
| operation | varchar(50) | NO | | 操作类型 |
| description | varchar(500) | YES | NULL | 操作描述 |
| request_method | varchar(10) | YES | NULL | 请求方法 |
| request_url | varchar(500) | YES | NULL | 请求URL |
| request_params | text | YES | NULL | 请求参数 |
| response_result | text | YES | NULL | 响应结果 |
| execution_time | int(11) | YES | NULL | 执行时长（毫秒） |
| ip_address | varchar(50) | YES | NULL | IP地址 |
| user_agent | varchar(500) | YES | NULL | 用户代理 |
| status | int(11) | YES | 1 | 状态（0:失败, 1:成功） |
| error_message | varchar(1000) | YES | NULL | 错误信息 |

**索引**:
- PRIMARY KEY (`id`)
- INDEX `idx_op_log_user` (`user_id`)
- INDEX `idx_op_log_module` (`module`)
- INDEX `idx_op_log_status` (`status`)

---

### 16. 系统配置表 (sys_config)

存储系统配置信息。

| 字段名 | 类型 | 允许NULL | 默认值 | 说明 |
|--------|------|----------|--------|------|
| id | int(11) | NO | AUTO_INCREMENT | 主键ID |
| config_key | varchar(100) | NO | | 配置键（唯一） |
| config_value | text | YES | NULL | 配置值 |
| config_type | varchar(20) | YES | 'string' | 配置类型（string, int, bool, json） |
| description | varchar(255) | YES | NULL | 配置描述 |
| group_name | varchar(50) | YES | NULL | 配置分组 |
| is_system | int(11) | YES | 0 | 是否系统配置（0:否, 1:是） |
| status | int(11) | YES | 1 | 状态（0:禁用, 1:启用） |
| sort | int(11) | YES | 0 | 排序 |

**索引**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_config_key` (`config_key`)
- INDEX `idx_config_key` (`config_key`)
- INDEX `idx_config_group` (`group_name`)
- INDEX `idx_config_status` (`status`)

---

### 17. 系统字典表 (sys_dict)

存储系统字典类型。

| 字段名 | 类型 | 允许NULL | 默认值 | 说明 |
|--------|------|----------|--------|------|
| id | int(11) | NO | AUTO_INCREMENT | 主键ID |
| name | varchar(100) | NO | | 字典名称 |
| code | varchar(100) | NO | | 字典编码（唯一） |
| description | varchar(500) | YES | NULL | 描述 |
| status | int(11) | YES | 1 | 状态（0:禁用, 1:启用） |
| sort | int(11) | YES | 0 | 排序 |

**索引**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_code` (`code`)
- INDEX `idx_dict_status` (`status`)
- INDEX `idx_dict_code` (`code`)

---

### 18. 系统字典项表 (sys_dict_item)

存储字典项数据。

| 字段名 | 类型 | 允许NULL | 默认值 | 说明 |
|--------|------|----------|--------|------|
| id | int(11) | NO | AUTO_INCREMENT | 主键ID |
| dict_id | int(11) | NO | | 字典ID（外键） |
| label | varchar(100) | NO | | 标签 |
| value | varchar(100) | NO | | 值 |
| color | varchar(50) | YES | NULL | 颜色 |
| description | varchar(500) | YES | NULL | 描述 |
| status | int(11) | YES | 1 | 状态（0:禁用, 1:启用） |
| sort | int(11) | YES | 0 | 排序 |

**索引**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_dict_value` (`dict_id`, `value`)
- INDEX `idx_dict_item_dict` (`dict_id`)
- INDEX `idx_dict_item_status` (`status`)

---

### 19. 数据权限规则表 (sys_data_permission_rule)

存储数据权限规则。

| 字段名 | 类型 | 允许NULL | 默认值 | 说明 |
|--------|------|----------|--------|------|
| id | int(11) | NO | AUTO_INCREMENT | 主键ID |
| name | varchar(100) | NO | | 规则名称 |
| code | varchar(100) | NO | | 规则编码（唯一） |
| permission_id | int(11) | NO | | 关联权限ID（外键） |
| resource_table | varchar(100) | NO | | 资源表名 |
| rule_type | int(11) | NO | | 规则类型（0:全部, 1:本部门, 2:本部门及下级, 3:仅本人, 4:自定义） |
| rule_expression | text | YES | NULL | 自定义规则表达式（SQL WHERE片段） |
| status | int(11) | YES | 1 | 状态（0:禁用, 1:启用） |
| description | varchar(500) | YES | NULL | 规则描述 |

**索引**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_code` (`code`)
- INDEX `idx_data_perm_permission` (`permission_id`)
- INDEX `idx_data_perm_status` (`status`)

---

## ER图关系说明

### 核心关系

```
sys_user (用户)
  ├── 1:1 → sys_user_profile (用户扩展信息)
  ├── 1:N → sys_user_role (用户角色)
  │       └── N:1 → sys_role (角色)
  │               ├── 1:N → sys_role_permission (角色权限)
  │               │       └── N:1 → sys_permission (权限)
  │               │               ├── 1:N → sys_menu_permission (菜单权限)
  │               │               │       └── N:1 → sys_menu (菜单)
  │               │               └── 1:N → sys_data_permission_rule (数据权限规则)
  │               └── 1:N → sys_user_group_role_relation (用户组角色)
  │                       └── N:1 → sys_user_group (用户组)
  │                               └── 1:N → sys_user_group_relation (用户组用户)
  │                                       └── N:1 → sys_user (用户)
  ├── N:1 → sys_dept (部门)
  └── 1:N → sys_user_session (用户会话)

sys_dept (部门)
  └── 1:N → sys_dept (子部门)

sys_dict (字典)
  └── 1:N → sys_dict_item (字典项)
```

---

## 使用说明

### 初始化数据库

1. 创建数据库：
```sql
CREATE DATABASE IF NOT EXISTS rbac_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 执行初始化脚本：
```bash
mysql -u root -p rbac_system < Scripts/init_schema.sql
```

### 注意事项

1. 所有表都支持软删除（通过 `is_deleted` 字段）
2. 所有表都支持多租户（通过 `tenant_id` 字段）
3. 使用乐观锁机制（`version` 字段）防止并发更新冲突
4. 建议定期清理已过期的用户会话和操作日志
5. 审计日志表建议定期归档

---

## 更新日志

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2026-04-13 | 初始版本，包含完整的RBAC系统数据库结构 |
