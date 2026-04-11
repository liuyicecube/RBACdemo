# 企业级RBAC系统 - API文档

## 目录
- [API概述](#api概述)
- [认证接口](#认证接口)
- [用户管理接口](#用户管理接口)
- [角色管理接口](#角色管理接口)
- [权限管理接口](#权限管理接口)
- [部门管理接口](#部门管理接口)
- [菜单管理接口](#菜单管理接口)
- [系统字典接口](#系统字典接口)
- [系统配置接口](#系统配置接口)
- [操作日志接口](#操作日志接口)
- [审计日志接口](#审计日志接口)
- [用户组接口](#用户组接口)
- [数据权限规则接口](#数据权限规则接口)
- [用户会话接口](#用户会话接口)
- [用户资料接口](#用户资料接口)
- [系统监控接口](#系统监控接口)
- [公共响应格式](#公共响应格式)
- [错误码说明](#错误码说明)

---

## API概述

### 基础信息

- **基础路径**：`/api/v1`
- **协议**：HTTP/HTTPS
- **数据格式**：JSON
- **字符编码**：UTF-8

### 认证方式

系统使用JWT（JSON Web Token）进行认证。

#### 认证流程

1. **登录获取Token**
   - 调用 `POST /api/v1/auth/login`
   - 获取 `access_token` 和 `refresh_token`

2. **使用Token访问API**
   - 在请求Header中添加：`Authorization: Bearer {access_token}`

3. **刷新Token**
   - 当 `access_token` 过期时
   - 调用 `POST /api/v1/auth/refresh`
   - 传入 `refresh_token` 获取新的 `access_token`

### 请求Header

```
Content-Type: application/json
Authorization: Bearer {access_token}
```

---

## 认证接口

### 用户登录

**接口**：`POST /api/v1/auth/login`

**标签**：认证管理

**权限**：无需权限

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |

**请求示例**：
```json
{
  "username": "admin",
  "password": "password123"
}
```

**响应示例**：
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 7200,
    "user": {
      "id": 1,
      "username": "admin",
      "nickname": "管理员",
      "email": "admin@example.com",
      "avatar": null,
      "roles": ["super_admin"]
    }
  }
}
```

**错误响应**：
```json
{
  "code": 401,
  "message": "用户名或密码错误",
  "data": null
}
```

---

### 用户注册

**接口**：`POST /api/v1/auth/register`

**标签**：认证管理

**权限**：无需权限

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |
| nickname | string | 是 | 昵称 |
| email | string | 否 | 邮箱 |
| phone | string | 否 | 手机号 |
| tenant_id | int | 否 | 租户ID（默认1） |

**请求示例**：
```json
{
  "username": "newuser",
  "password": "password123",
  "nickname": "新用户",
  "email": "newuser@example.com",
  "phone": "13800138000"
}
```

**响应示例**：
```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "id": 2,
    "username": "newuser",
    "nickname": "新用户",
    "email": "newuser@example.com",
    "phone": "13800138000"
  }
}
```

---

### 刷新Token

**接口**：`POST /api/v1/auth/refresh`

**标签**：认证管理

**权限**：无需权限

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| refresh_token | string | 是 | 刷新令牌 |

**请求示例**：
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**响应示例**：
```json
{
  "code": 200,
  "message": "Token刷新成功",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 7200
  }
}
```

---

### 修改密码

**接口**：`POST /api/v1/auth/change-password`

**标签**：认证管理

**权限**：需要登录

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| old_password | string | 是 | 旧密码 |
| new_password | string | 是 | 新密码 |

**请求示例**：
```json
{
  "old_password": "oldpass123",
  "new_password": "newpass456"
}
```

**响应示例**：
```json
{
  "code": 200,
  "message": "密码修改成功",
  "data": null
}
```

---

### 重置密码

**接口**：`POST /api/v1/auth/reset-password`

**标签**：认证管理

**权限**：需要管理员权限

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| user_id | int | 是 | 用户ID |
| new_password | string | 是 | 新密码 |

**请求示例**：
```json
{
  "user_id": 2,
  "new_password": "resetpass123"
}
```

**响应示例**：
```json
{
  "code": 200,
  "message": "密码重置成功",
  "data": null
}
```

---

## 用户管理接口

### 获取用户列表

**接口**：`GET /api/v1/users`

**标签**：用户管理

**权限**：`user:view`

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| keyword | string | 否 | 搜索关键词（用户名/昵称/邮箱/手机号） |
| department_id | int | 否 | 部门ID |
| status | int | 否 | 状态（1启用 0禁用） |
| page | int | 否 | 页码（默认1） |
| page_size | int | 否 | 每页数量（默认10） |

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
      "avatar": "http://example.com/avatar.jpg",
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

---

### 获取用户详情

**接口**：`GET /api/v1/users/{user_id}`

**标签**：用户管理

**权限**：`user:view`

**路径参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| user_id | int | 是 | 用户ID |

**响应示例**：
```json
{
  "code": 200,
  "message": "获取用户详情成功",
  "data": {
    "id": 1,
    "username": "admin",
    "nickname": "管理员",
    "email": "admin@example.com",
    "phone": "13800138000",
    "avatar": "http://example.com/avatar.jpg",
    "department_id": 1,
    "status": 1,
    "last_login_time": "2026-04-11 10:00:00",
    "last_login_ip": "192.168.1.1",
    "create_time": "2026-04-01 00:00:00",
    "update_time": "2026-04-11 10:00:00",
    "roles": [
      {
        "id": 1,
        "name": "超级管理员",
        "code": "super_admin"
      }
    ]
  }
}
```

---

### 创建用户

**接口**：`POST /api/v1/users`

**标签**：用户管理

**权限**：`user:create`

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |
| nickname | string | 是 | 昵称 |
| email | string | 否 | 邮箱 |
| phone | string | 否 | 手机号 |
| avatar | string | 否 | 头像URL |
| department_id | int | 否 | 部门ID |
| status | int | 否 | 状态（默认1启用） |

**请求示例**：
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

**响应示例**：
```json
{
  "code": 200,
  "message": "创建用户成功",
  "data": {
    "id": 2,
    "username": "newuser",
    "nickname": "新用户",
    "email": "newuser@example.com",
    "phone": "13800138001",
    "department_id": 1,
    "status": 1,
    "create_time": "2026-04-11 10:00:00",
    "update_time": "2026-04-11 10:00:00"
  }
}
```

---

### 更新用户

**接口**：`PUT /api/v1/users/{user_id}`

**标签**：用户管理

**权限**：`user:update`

**路径参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| user_id | int | 是 | 用户ID |

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| nickname | string | 否 | 昵称 |
| email | string | 否 | 邮箱 |
| phone | string | 否 | 手机号 |
| avatar | string | 否 | 头像URL |
| department_id | int | 否 | 部门ID |
| status | int | 否 | 状态 |

**请求示例**：
```json
{
  "nickname": "更新后的昵称",
  "email": "updated@example.com",
  "status": 1
}
```

**响应示例**：
```json
{
  "code": 200,
  "message": "更新用户成功",
  "data": {
    "id": 2,
    "username": "newuser",
    "nickname": "更新后的昵称",
    "email": "updated@example.com",
    "update_time": "2026-04-11 10:30:00"
  }
}
```

---

### 删除用户

**接口**：`DELETE /api/v1/users/{user_id}`

**标签**：用户管理

**权限**：`user:delete`

**路径参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| user_id | int | 是 | 用户ID |

**响应示例**：
```json
{
  "code": 200,
  "message": "删除用户成功",
  "data": null
}
```

---

### 分配角色给用户

**接口**：`POST /api/v1/users/{user_id}/roles`

**标签**：用户管理

**权限**：`user:update`

**路径参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| user_id | int | 是 | 用户ID |

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| role_ids | array[int] | 是 | 角色ID列表 |

**请求示例**：
```json
{
  "role_ids": [1, 2, 3]
}
```

**响应示例**：
```json
{
  "code": 200,
  "message": "分配角色成功",
  "data": null
}
```

---

### 设置用户主角色

**接口**：`POST /api/v1/users/{user_id}/primary-role`

**标签**：用户管理

**权限**：`user:update`

**路径参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| user_id | int | 是 | 用户ID |

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| role_id | int | 是 | 主角色ID |

**请求示例**：
```json
{
  "role_id": 1
}
```

**响应示例**：
```json
{
  "code": 200,
  "message": "设置主角色成功",
  "data": null
}
```

---

### 启用/禁用用户

**接口**：`POST /api/v1/users/{user_id}/status`

**标签**：用户管理

**权限**：`user:update`

**路径参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| user_id | int | 是 | 用户ID |

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| status | int | 是 | 状态（1启用 0禁用） |

**请求示例**：
```json
{
  "status": 0
}
```

**响应示例**：
```json
{
  "code": 200,
  "message": "更新用户状态成功",
  "data": null
}
```

---

## 角色管理接口

### 获取角色列表

**接口**：`GET /api/v1/roles`

**标签**：角色管理

**权限**：`role:view`

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| keyword | string | 否 | 搜索关键词 |
| status | int | 否 | 状态（1启用 0禁用） |
| page | int | 否 | 页码（默认1） |
| page_size | int | 否 | 每页数量（默认10） |

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

---

### 获取所有启用的角色

**接口**：`GET /api/v1/roles/all`

**标签**：角色管理

**权限**：`role:view`

**响应示例**：
```json
{
  "code": 200,
  "message": "获取所有启用的角色成功",
  "data": [
    {
      "id": 1,
      "name": "超级管理员",
      "code": "super_admin"
    },
    {
      "id": 2,
      "name": "管理员",
      "code": "admin"
    }
  ]
}
```

---

### 获取角色详情

**接口**：`GET /api/v1/roles/{role_id}`

**标签**：角色管理

**权限**：`role:view`

**路径参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| role_id | int | 是 | 角色ID |

**响应示例**：
```json
{
  "code": 200,
  "message": "获取角色详情成功",
  "data": {
    "id": 1,
    "name": "超级管理员",
    "code": "super_admin",
    "description": "拥有所有权限",
    "sort_order": 1,
    "status": 1,
    "create_time": "2026-04-01 00:00:00",
    "update_time": "2026-04-11 10:00:00",
    "permissions": [
      {
        "id": 1,
        "name": "查看用户",
        "code": "user:view"
      }
    ]
  }
}
```

---

### 创建角色

**接口**：`POST /api/v1/roles`

**标签**：角色管理

**权限**：`role:create`

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| name | string | 是 | 角色名称 |
| code | string | 是 | 角色编码 |
| description | string | 否 | 角色描述 |
| sort_order | int | 否 | 排序（默认0） |
| status | int | 否 | 状态（默认1启用） |

**请求示例**：
```json
{
  "name": "新角色",
  "code": "new_role",
  "description": "这是一个新角色",
  "sort_order": 10,
  "status": 1
}
```

**响应示例**：
```json
{
  "code": 200,
  "message": "创建角色成功",
  "data": {
    "id": 3,
    "name": "新角色",
    "code": "new_role",
    "description": "这是一个新角色",
    "sort_order": 10,
    "status": 1,
    "create_time": "2026-04-11 10:00:00",
    "update_time": "2026-04-11 10:00:00"
  }
}
```

---

### 更新角色

**接口**：`PUT /api/v1/roles/{role_id}`

**标签**：角色管理

**权限**：`role:update`

**路径参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| role_id | int | 是 | 角色ID |

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| name | string | 否 | 角色名称 |
| description | string | 否 | 角色描述 |
| sort_order | int | 否 | 排序 |
| status | int | 否 | 状态 |

**请求示例**：
```json
{
  "name": "更新后的角色名",
  "description": "更新后的描述",
  "status": 1
}
```

**响应示例**：
```json
{
  "code": 200,
  "message": "更新角色成功",
  "data": {
    "id": 3,
    "name": "更新后的角色名",
    "update_time": "2026-04-11 10:30:00"
  }
}
```

---

### 删除角色

**接口**：`DELETE /api/v1/roles/{role_id}`

**标签**：角色管理

**权限**：`role:delete`

**路径参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| role_id | int | 是 | 角色ID |

**响应示例**：
```json
{
  "code": 200,
  "message": "删除角色成功",
  "data": null
}
```

---

### 分配权限给角色

**接口**：`POST /api/v1/roles/{role_id}/permissions`

**标签**：角色管理

**权限**：`role:update`

**路径参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| role_id | int | 是 | 角色ID |

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| permission_ids | array[int] | 是 | 权限ID列表 |

**请求示例**：
```json
{
  "permission_ids": [1, 2, 3, 4, 5]
}
```

**响应示例**：
```json
{
  "code": 200,
  "message": "分配权限成功",
  "data": null
}
```

---

### 启用/禁用角色

**接口**：`POST /api/v1/roles/{role_id}/status`

**标签**：角色管理

**权限**：`role:update`

**路径参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| role_id | int | 是 | 角色ID |

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| status | int | 是 | 状态（1启用 0禁用） |

**请求示例**：
```json
{
  "status": 0
}
```

**响应示例**：
```json
{
  "code": 200,
  "message": "更新角色状态成功",
  "data": null
}
```

---

## 权限管理接口

### 获取权限列表

**接口**：`GET /api/v1/permissions`

**标签**：权限管理

**权限**：`permission:view`

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| keyword | string | 否 | 搜索关键词 |
| type | int | 否 | 权限类型 |
| resource_type | string | 否 | 资源类型 |
| action | string | 否 | 操作类型 |
| status | int | 否 | 状态 |
| parent_id | int | 否 | 父权限ID |
| page | int | 否 | 页码（默认1） |
| page_size | int | 否 | 每页数量（默认10） |

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

---

### 获取所有启用的权限

**接口**：`GET /api/v1/permissions/all`

**标签**：权限管理

**权限**：`permission:view`

**响应示例**：
```json
{
  "code": 200,
  "message": "获取所有启用的权限成功",
  "data": [
    {
      "id": 1,
      "name": "查看用户",
      "code": "user:view",
      "type": 1,
      "parent_id": null
    },
    {
      "id": 2,
      "name": "创建用户",
      "code": "user:create",
      "type": 1,
      "parent_id": null
    }
  ]
}
```

---

### 获取权限树形结构

**接口**：`GET /api/v1/permissions/tree`

**标签**：权限管理

**权限**：`permission:view`

**响应示例**：
```json
{
  "code": 200,
  "message": "获取权限树成功",
  "data": [
    {
      "id": 1,
      "name": "用户管理",
      "code": "user",
      "children": [
        {
          "id": 2,
          "name": "查看用户",
          "code": "user:view",
          "children": []
        },
        {
          "id": 3,
          "name": "创建用户",
          "code": "user:create",
          "children": []
        }
      ]
    }
  ]
}
```

---

### 获取权限详情

**接口**：`GET /api/v1/permissions/{permission_id}`

**标签**：权限管理

**权限**：`permission:view`

**路径参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| permission_id | int | 是 | 权限ID |

**响应示例**：
```json
{
  "code": 200,
  "message": "获取权限详情成功",
  "data": {
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
}
```

---

### 创建权限

**接口**：`POST /api/v1/permissions`

**标签**：权限管理

**权限**：`permission:create`

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| name | string | 是 | 权限名称 |
| code | string | 是 | 权限编码 |
| type | int | 是 | 权限类型 |
| resource_type | string | 否 | 资源类型 |
| resource_id | int | 否 | 资源ID |
| action | string | 否 | 操作类型 |
| path | string | 否 | API路径 |
| method | string | 否 | HTTP方法 |
| parent_id | int | 否 | 父权限ID |
| level | int | 否 | 层级 |
| status | int | 否 | 状态（默认1启用） |

**请求示例**：
```json
{
  "name": "新权限",
  "code": "new:permission",
  "type": 1,
  "resource_type": "new_resource",
  "action": "view",
  "path": "/api/v1/new-resource",
  "method": "GET",
  "status": 1
}
```

**响应示例**：
```json
{
  "code": 200,
  "message": "创建权限成功",
  "data": {
    "id": 101,
    "name": "新权限",
    "code": "new:permission",
    "status": 1,
    "create_time": "2026-04-11 10:00:00",
    "update_time": "2026-04-11 10:00:00"
  }
}
```

---

### 更新权限

**接口**：`PUT /api/v1/permissions/{permission_id}`

**标签**：权限管理

**权限**：`permission:update`

**路径参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| permission_id | int | 是 | 权限ID |

**请求参数**：参考创建权限

**响应示例**：
```json
{
  "code": 200,
  "message": "更新权限成功",
  "data": {
    "id": 101,
    "name": "更新后的权限名",
    "update_time": "2026-04-11 10:30:00"
  }
}
```

---

### 删除权限

**接口**：`DELETE /api/v1/permissions/{permission_id}`

**标签**：权限管理

**权限**：`permission:delete`

**路径参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| permission_id | int | 是 | 权限ID |

**响应示例**：
```json
{
  "code": 200,
  "message": "删除权限成功",
  "data": null
}
```

---

## 部门管理接口

### 获取部门列表

**接口**：`GET /api/v1/departments`

**标签**：部门管理

**权限**：`department:view`

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| keyword | string | 否 | 搜索关键词 |
| status | int | 否 | 状态 |
| parent_id | int | 否 | 父部门ID |
| page | int | 否 | 页码（默认1） |
| page_size | int | 否 | 每页数量（默认10） |

**响应示例**：
```json
{
  "code": 200,
  "message": "获取部门列表成功",
  "data": [
    {
      "id": 1,
      "name": "总公司",
      "code": "HQ",
      "parent_id": null,
      "level": 1,
      "description": "总公司",
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

---

### 获取部门树形结构

**接口**：`GET /api/v1/departments/tree`

**标签**：部门管理

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
        },
        {
          "id": 3,
          "name": "运营部",
          "code": "OPS",
          "children": []
        }
      ]
    }
  ]
}
```

---

### 获取部门详情

**接口**：`GET /api/v1/departments/{department_id}`

**标签**：部门管理

**权限**：`department:view`

**路径参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| department_id | int | 是 | 部门ID |

---

### 创建部门

**接口**：`POST /api/v1/departments`

**标签**：部门管理

**权限**：`department:create`

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| name | string | 是 | 部门名称 |
| code | string | 是 | 部门编码 |
| parent_id | int | 否 | 父部门ID |
| level | int | 否 | 层级 |
| description | string | 否 | 部门描述 |
| status | int | 否 | 状态（默认1启用） |

---

### 更新部门

**接口**：`PUT /api/v1/departments/{department_id}`

**标签**：部门管理

**权限**：`department:update`

---

### 删除部门

**接口**：`DELETE /api/v1/departments/{department_id}`

**标签**：部门管理

**权限**：`department:delete`

---

## 菜单管理接口

### 获取菜单列表

**接口**：`GET /api/v1/menus`

**标签**：菜单管理

**权限**：`menu:view`

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| keyword | string | 否 | 搜索关键词 |
| status | int | 否 | 状态 |
| parent_id | int | 否 | 父菜单ID |
| page | int | 否 | 页码 |
| page_size | int | 否 | 每页数量 |

---

### 获取菜单树形结构

**接口**：`GET /api/v1/menus/tree`

**标签**：菜单管理

**权限**：`menu:view`

---

### 获取当前用户菜单

**接口**：`GET /api/v1/menus/my`

**标签**：菜单管理

**权限**：需要登录

---

### 创建菜单

**接口**：`POST /api/v1/menus`

**标签**：菜单管理

**权限**：`menu:create`

---

### 更新菜单

**接口**：`PUT /api/v1/menus/{menu_id}`

**标签**：菜单管理

**权限**：`menu:update`

---

### 删除菜单

**接口**：`DELETE /api/v1/menus/{menu_id}`

**标签**：菜单管理

**权限**：`menu:delete`

---

## 系统字典接口

### 获取字典列表

**接口**：`GET /api/v1/system-dicts`

**标签**：系统字典

**权限**：`dict:view`

---

### 获取字典树形结构

**接口**：`GET /api/v1/system-dicts/tree`

**标签**：系统字典

**权限**：`dict:view`

---

### 创建字典

**接口**：`POST /api/v1/system-dicts`

**标签**：系统字典

**权限**：`dict:create`

---

### 更新字典

**接口**：`PUT /api/v1/system-dicts/{dict_id}`

**标签**：系统字典

**权限**：`dict:update`

---

### 删除字典

**接口**：`DELETE /api/v1/system-dicts/{dict_id}`

**标签**：系统字典

**权限**：`dict:delete`

---

## 系统配置接口

### 获取配置列表

**接口**：`GET /api/v1/system-configs`

**标签**：系统配置

**权限**：`config:view`

---

### 获取配置详情

**接口**：`GET /api/v1/system-configs/{config_id}`

**标签**：系统配置

**权限**：`config:view`

---

### 创建配置

**接口**：`POST /api/v1/system-configs`

**标签**：系统配置

**权限**：`config:create`

---

### 更新配置

**接口**：`PUT /api/v1/system-configs/{config_id}`

**标签**：系统配置

**权限**：`config:update`

---

### 删除配置

**接口**：`DELETE /api/v1/system-configs/{config_id}`

**标签**：系统配置

**权限**：`config:delete`

---

## 操作日志接口

### 获取操作日志列表

**接口**：`GET /api/v1/operation-logs`

**标签**：操作日志

**权限**：`log:view`

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| keyword | string | 否 | 搜索关键词 |
| user_id | int | 否 | 用户ID |
| module | string | 否 | 模块 |
| action | string | 否 | 操作类型 |
| start_time | string | 否 | 开始时间 |
| end_time | string | 否 | 结束时间 |
| page | int | 否 | 页码 |
| page_size | int | 否 | 每页数量 |

---

### 获取操作日志详情

**接口**：`GET /api/v1/operation-logs/{log_id}`

**标签**：操作日志

**权限**：`log:view`

---

## 审计日志接口

### 获取审计日志列表

**接口**：`GET /api/v1/audit-logs`

**标签**：审计日志

**权限**：`audit:view`

**请求参数**：参考操作日志

---

### 获取审计日志详情

**接口**：`GET /api/v1/audit-logs/{log_id}`

**标签**：审计日志

**权限**：`audit:view`

---

## 用户组接口

### 获取用户组列表

**接口**：`GET /api/v1/user-groups`

**标签**：用户组

**权限**：`user_group:view`

---

### 获取用户组详情

**接口**：`GET /api/v1/user-groups/{group_id}`

**标签**：用户组

**权限**：`user_group:view`

---

### 创建用户组

**接口**：`POST /api/v1/user-groups`

**标签**：用户组

**权限**：`user_group:create`

---

### 更新用户组

**接口**：`PUT /api/v1/user-groups/{group_id}`

**标签**：用户组

**权限**：`user_group:update`

---

### 删除用户组

**接口**：`DELETE /api/v1/user-groups/{group_id}`

**标签**：用户组

**权限**：`user_group:delete`

---

### 分配用户到用户组

**接口**：`POST /api/v1/user-groups/{group_id}/users`

**标签**：用户组

**权限**：`user_group:update`

---

### 分配角色到用户组

**接口**：`POST /api/v1/user-groups/{group_id}/roles`

**标签**：用户组

**权限**：`user_group:update`

---

## 数据权限规则接口

### 获取数据权限规则列表

**接口**：`GET /api/v1/data-permission-rules`

**标签**：数据权限规则

**权限**：`data_rule:view`

---

### 创建数据权限规则

**接口**：`POST /api/v1/data-permission-rules`

**标签**：数据权限规则

**权限**：`data_rule:create`

---

### 更新数据权限规则

**接口**：`PUT /api/v1/data-permission-rules/{rule_id}`

**标签**：数据权限规则

**权限**：`data_rule:update`

---

### 删除数据权限规则

**接口**：`DELETE /api/v1/data-permission-rules/{rule_id}`

**标签**：数据权限规则

**权限**：`data_rule:delete`

---

## 用户会话接口

### 获取用户会话列表

**接口**：`GET /api/v1/user-sessions`

**标签**：用户会话

**权限**：`session:view`

---

### 强制用户下线

**接口**：`POST /api/v1/user-sessions/{session_id}/kick`

**标签**：用户会话

**权限**：`session:manage`

---

## 用户资料接口

### 获取当前用户资料

**接口**：`GET /api/v1/user-profiles`

**标签**：用户资料

**权限**：需要登录

---

### 更新用户资料

**接口**：`PUT /api/v1/user-profiles`

**标签**：用户资料

**权限**：需要登录

---

### 上传头像

**接口**：`POST /api/v1/user-profiles/avatar`

**标签**：用户资料

**权限**：需要登录

**请求类型**：multipart/form-data

---

## 系统监控接口

### 获取系统指标

**接口**：`GET /api/v1/metrics`

**标签**：系统监控

**权限**：`metrics:view`

**响应示例**：
```json
{
  "code": 200,
  "message": "获取系统指标成功",
  "data": {
    "cpu": {
      "usage": 45.5,
      "cores": 8
    },
    "memory": {
      "total": 16384,
      "used": 8192,
      "usage": 50.0
    },
    "disk": {
      "total": 1024000,
      "used": 512000,
      "usage": 50.0
    },
    "network": {
      "in": 1024000,
      "out": 512000
    },
    "api": {
      "total_requests": 10000,
      "success_rate": 99.5,
      "avg_response_time": 50
    }
  }
}
```

---

## 公共响应格式

### 成功响应

```json
{
  "code": 200,
  "message": "操作成功",
  "data": {}
}
```

### 分页响应

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

### 错误响应

```json
{
  "code": 400,
  "message": "错误信息",
  "data": null,
  "error_code": 40000
}
```

---

## 错误码说明

### HTTP状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 401 | 未授权/Token无效 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

### 业务错误码

| 错误码 | 说明 |
|--------|------|
| 40000 | 参数错误 |
| 40100 | 未登录 |
| 40101 | Token无效 |
| 40102 | Token过期 |
| 40300 | 权限不足 |
| 40400 | 资源不存在 |
| 40900 | 资源已存在 |
| 50000 | 服务器内部错误 |

---

## 附录

### 权限编码规范

权限编码格式：`{resource}:{action}`

示例：
- `user:view` - 查看用户
- `user:create` - 创建用户
- `user:update` - 更新用户
- `user:delete` - 删除用户
- `role:view` - 查看角色
- `role:create` - 创建角色

### 日期时间格式

所有日期时间使用ISO 8601格式：
- `YYYY-MM-DD HH:MM:SS`
- 示例：`2026-04-11 10:00:00`

### 分页参数说明

- `page`：页码，从1开始
- `page_size`：每页数量，建议10-50
- `total`：总记录数

---

## 更新日志

### v1.0.0 (2026-04-11)
- 初始版本发布
- 包含所有核心API接口文档
