# 企业级RBAC系统 - 用户文档

## 目录
- [系统概述](#系统概述)
- [快速开始](#快速开始)
- [用户管理](#用户管理)
- [角色管理](#角色管理)
- [权限管理](#权限管理)
- [部门管理](#部门管理)
- [菜单管理](#菜单管理)
- [其他功能](#其他功能)
- [常见问题](#常见问题)

---

## 系统概述

### 系统简介

企业级RBAC（基于角色的访问控制）系统是一个完整的用户权限管理解决方案，提供用户、角色、权限、部门等核心功能的管理。

### 主要功能

- **认证管理**：用户登录、注册、Token刷新
- **用户管理**：用户增删改查、状态管理、角色分配
- **角色管理**：角色增删改查、权限分配
- **权限管理**：权限增删改查、树形结构
- **部门管理**：部门增删改查、树形结构
- **菜单管理**：菜单增删改查、树形结构
- **系统配置**：系统参数配置
- **操作日志**：用户操作记录
- **审计日志**：系统审计记录
- **用户组管理**：用户组管理
- **数据权限**：数据权限规则
- **系统监控**：系统指标监控

### 技术栈

- **后端框架**：FastAPI
- **数据库**：SQLAlchemy
- **认证**：JWT Token

---

## 快速开始

### API基础路径

所有API的基础路径为：`/api/v1`

### 认证方式

系统使用JWT Token进行认证：

1. 使用 `/api/v1/auth/login` 接口登录获取 access_token 和 refresh_token
2. 在后续请求的 Header 中添加：`Authorization: Bearer {access_token}`
3. Token过期后使用 `/api/v1/auth/refresh` 刷新Token

### 响应格式

所有API响应格式统一：

```json
{
  "code": 200,
  "message": "操作成功",
  "data": {}
}
```

分页响应格式：

```json
{
  "code": 200,
  "message": "获取成功",
  "data": [],
  "page": 1,
  "page_size": 10,
  "total": 100
}
```

---

## 用户管理

### 用户列表

**接口**：`GET /api/v1/users`

**权限**：`user:view`

**请求参数**：
- `keyword`（可选）：搜索关键词（用户名/昵称/邮箱/手机号）
- `department_id`（可选）：部门ID
- `status`（可选）：状态（1启用 0禁用）
- `page`：页码（默认1）
- `page_size`：每页数量（默认10）

**响应示例**：
```json
{
  "code": 200,
  "message": "获取用户列表成功",
  "data": [
    {
      "id": 1,
      "username": "admin",
      "nickname": "管理员",
      "email": "admin@example.com",
      "phone": "13800138000",
      "avatar": "http://...",
      "department_id": 1,
      "status": 1,
      "last_login_time": "2026-04-11 10:00:00",
      "last_login_ip": "192.168.1.1",
      "create_time": "2026-04-01 00:00:00",
      "update_time": "2026-04-11 10:00:00"
    }
  ],
  "page": 1,
  "page_size": 10,
  "total": 100
}
```

### 用户详情

**接口**：`GET /api/v1/users/{user_id}`

**权限**：`user:view`

**路径参数**：
- `user_id`：用户ID

### 创建用户

**接口**：`POST /api/v1/users`

**权限**：`user:create`

**请求体**：
```json
{
  "username": "newuser",
  "password": "password123",
  "nickname": "新用户",
  "email": "newuser@example.com",
  "phone": "13800138001",
  "department_id": 1,
  "status": 1
}
```

### 更新用户

**接口**：`PUT /api/v1/users/{user_id}`

**权限**：`user:update`

### 删除用户

**接口**：`DELETE /api/v1/users/{user_id}`

**权限**：`user:delete`

### 分配角色

**接口**：`POST /api/v1/users/{user_id}/roles`

**权限**：`user:update`

**请求体**：
```json
{
  "role_ids": [1, 2, 3]
}
```

---

## 角色管理

### 角色列表

**接口**：`GET /api/v1/roles`

**权限**：`role:view`

**请求参数**：
- `keyword`（可选）：搜索关键词
- `status`（可选）：状态（1启用 0禁用）
- `page`：页码
- `page_size`：每页数量

**响应示例**：
```json
{
  "code": 200,
  "message": "获取角色列表成功",
  "data": [
    {
      "id": 1,
      "name": "超级管理员",
      "code": "super_admin",
      "description": "拥有所有权限",
      "sort_order": 1,
      "status": 1,
      "create_time": "2026-04-01 00:00:00",
      "update_time": "2026-04-11 10:00:00"
    }
  ],
  "page": 1,
  "page_size": 10,
  "total": 10
}
```

### 所有启用角色

**接口**：`GET /api/v1/roles/all`

**权限**：`role:view`

**用途**：用于下拉选择，只返回启用的角色

### 创建角色

**接口**：`POST /api/v1/roles`

**权限**：`role:create`

**请求体**：
```json
{
  "name": "新角色",
  "code": "new_role",
  "description": "角色描述",
  "sort_order": 10,
  "status": 1
}
```

### 更新角色

**接口**：`PUT /api/v1/roles/{role_id}`

**权限**：`role:update`

### 删除角色

**接口**：`DELETE /api/v1/roles/{role_id}`

**权限**：`role:delete`

### 分配权限

**接口**：`POST /api/v1/roles/{role_id}/permissions`

**权限**：`role:update`

**请求体**：
```json
{
  "permission_ids": [1, 2, 3, 4, 5]
}
```

---

## 权限管理

### 权限列表

**接口**：`GET /api/v1/permissions`

**权限**：`permission:view`

**请求参数**：
- `keyword`（可选）：搜索关键词
- `type`（可选）：权限类型
- `resource_type`（可选）：资源类型
- `action`（可选）：操作类型
- `status`（可选）：状态
- `parent_id`（可选）：父权限ID
- `page`：页码
- `page_size`：每页数量

**响应示例**：
```json
{
  "code": 200,
  "message": "获取权限列表成功",
  "data": [
    {
      "id": 1,
      "name": "查看用户",
      "code": "user:view",
      "type": 1,
      "resource_type": "user",
      "resource_id": null,
      "action": "view",
      "path": "/api/v1/users",
      "method": "GET",
      "parent_id": null,
      "level": 1,
      "status": 1,
      "create_time": "2026-04-01 00:00:00",
      "update_time": "2026-04-11 10:00:00"
    }
  ],
  "page": 1,
  "page_size": 10,
  "total": 100
}
```

### 所有启用权限

**接口**：`GET /api/v1/permissions/all`

**权限**：`permission:view`

**用途**：用于分配权限，只返回启用的权限

### 创建权限

**接口**：`POST /api/v1/permissions`

**权限**：`permission:create`

### 更新权限

**接口**：`PUT /api/v1/permissions/{permission_id}`

**权限**：`permission:update`

### 删除权限

**接口**：`DELETE /api/v1/permissions/{permission_id}`

**权限**：`permission:delete`

---

## 部门管理

### 部门列表

**接口**：`GET /api/v1/departments`

**权限**：`department:view`

**请求参数**：
- `keyword`（可选）：搜索关键词
- `status`（可选）：状态
- `parent_id`（可选）：父部门ID
- `page`：页码
- `page_size`：每页数量

### 部门树形结构

**接口**：`GET /api/v1/departments/tree`

**权限**：`department:view`

**响应示例**：
```json
{
  "code": 200,
  "message": "获取部门树成功",
  "data": [
    {
      "id": 1,
      "name": "总公司",
      "code": "HQ",
      "children": [
        {
          "id": 2,
          "name": "技术部",
          "code": "TECH",
          "children": []
        }
      ]
    }
  ]
}
```

### 创建部门

**接口**：`POST /api/v1/departments`

**权限**：`department:create`

### 更新部门

**接口**：`PUT /api/v1/departments/{department_id}`

**权限**：`department:update`

### 删除部门

**接口**：`DELETE /api/v1/departments/{department_id}`

**权限**：`department:delete`

---

## 菜单管理

### 菜单列表

**接口**：`GET /api/v1/menus`

**权限**：`menu:view`

### 菜单树形结构

**接口**：`GET /api/v1/menus/tree`

**权限**：`menu:view`

### 创建菜单

**接口**：`POST /api/v1/menus`

**权限**：`menu:create`

### 更新菜单

**接口**：`PUT /api/v1/menus/{menu_id}`

**权限**：`menu:update`

### 删除菜单

**接口**：`DELETE /api/v1/menus/{menu_id}`

**权限**：`menu:delete`

---

## 其他功能

### 认证管理

**登录**：`POST /api/v1/auth/login`

**请求体**：
```json
{
  "username": "admin",
  "password": "password123"
}
```

**响应**：
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "user": {
      "id": 1,
      "username": "admin",
      "nickname": "管理员"
    }
  }
}
```

**注册**：`POST /api/v1/auth/register`

**刷新Token**：`POST /api/v1/auth/refresh`

**修改密码**：`POST /api/v1/auth/change-password`

**重置密码**：`POST /api/v1/auth/reset-password`

### 系统字典

**列表**：`GET /api/v1/system-dicts`

**树形**：`GET /api/v1/system-dicts/tree`

**创建**：`POST /api/v1/system-dicts`

**更新**：`PUT /api/v1/system-dicts/{dict_id}`

**删除**：`DELETE /api/v1/system-dicts/{dict_id}`

### 系统配置

**列表**：`GET /api/v1/system-configs`

**创建**：`POST /api/v1/system-configs`

**更新**：`PUT /api/v1/system-configs/{config_id}`

**删除**：`DELETE /api/v1/system-configs/{config_id}`

### 操作日志

**列表**：`GET /api/v1/operation-logs`

**权限**：`log:view`

### 审计日志

**列表**：`GET /api/v1/audit-logs`

**权限**：`audit:view`

### 用户组管理

**列表**：`GET /api/v1/user-groups`

**创建**：`POST /api/v1/user-groups`

**更新**：`PUT /api/v1/user-groups/{group_id}`

**删除**：`DELETE /api/v1/user-groups/{group_id}`

### 数据权限规则

**列表**：`GET /api/v1/data-permission-rules`

**创建**：`POST /api/v1/data-permission-rules`

**更新**：`PUT /api/v1/data-permission-rules/{rule_id}`

**删除**：`DELETE /api/v1/data-permission-rules/{rule_id}`

### 用户会话

**列表**：`GET /api/v1/user-sessions`

**强制下线**：`POST /api/v1/user-sessions/{session_id}/kick`

### 用户资料

**获取**：`GET /api/v1/user-profiles`

**更新**：`PUT /api/v1/user-profiles`

**上传头像**：`POST /api/v1/user-profiles/avatar`

### 系统监控

**指标**：`GET /api/v1/metrics`

---

## 常见问题

### Q: Token过期了怎么办？

A: 使用 `/api/v1/auth/refresh` 接口，传入 refresh_token 获取新的 access_token。

### Q: 如何获取当前登录用户信息？

A: 登录成功后，响应中会包含用户信息。也可以通过解码 access_token 获取。

### Q: 权限检查失败怎么办？

A: 确认：
1. 用户是否拥有对应的角色
2. 角色是否分配了对应的权限
3. 权限的 resource_type 和 action 是否正确

### Q: 分页参数如何使用？

A: 使用 `page` 和 `page_size` 参数，响应中会返回 `total` 总数。

---

## 联系方式

如有问题，请联系技术支持团队。
