# 企业级RBAC系统 - 前端开发师使用文档

## 目录
- [文档概述](#文档概述)
- [快速开始](#快速开始)
- [API基础配置](#api基础配置)
- [认证流程](#认证流程)
- [API请求封装](#api请求封装)
- [各模块接口调用示例](#各模块接口调用示例)
- [状态管理方案](#状态管理方案)
- [路由守卫](#路由守卫)
- [错误处理](#错误处理)
- [权限控制](#权限控制)
- [常见组件封装](#常见组件封装)
- [最佳实践](#最佳实践)
- [常见问题](#常见问题)

---

## 文档概述

### 面向人群

本文档专门为前端开发人员编写，帮助你快速集成和使用企业级RBAC系统的后端API。

### 前置要求

- 熟悉现代前端框架（Vue.js / React / Angular 等）
- 了解 HTTP 请求和 RESTful API
- 了解 JWT 认证机制

### 技术栈建议

| 分类 | 推荐技术 |
|------|----------|
| UI框架 | Vue 3 / React 18 |
| HTTP客户端 | Axios |
| 状态管理 | Pinia / Redux Toolkit |
| 路由 | Vue Router / React Router |
| UI组件库 | Element Plus / Ant Design |

---

## 快速开始

### 1. 环境准备

确保后端服务已启动并运行在：
```
http://localhost:8000
```

API基础路径：
```
http://localhost:8000/api/v1
```

### 2. 安装依赖

```bash
# 使用 npm
npm install axios

# 使用 yarn
yarn add axios

# 使用 pnpm
pnpm add axios
```

### 3. 最简单的API调用示例

```javascript
import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  timeout: 10000
});

// 登录
async function login() {
  try {
    const response = await api.post('/auth/login', {
      username: 'admin',
      password: 'password123'
    });
    
    const { access_token, refresh_token, user } = response.data.data;
    
    // 保存token
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    localStorage.setItem('user', JSON.stringify(user));
    
    console.log('登录成功', user);
  } catch (error) {
    console.error('登录失败', error);
  }
}

// 调用需要认证的接口
async function getUsers() {
  try {
    const token = localStorage.getItem('access_token');
    
    const response = await api.get('/users', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    
    console.log('用户列表', response.data.data);
  } catch (error) {
    console.error('获取用户列表失败', error);
  }
}
```

---

## API基础配置

### 完整的Axios配置

```javascript
// src/utils/request.js
import axios from 'axios';
import { ElMessage } from 'element-plus';
import router from '@/router';

// 创建axios实例
const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json;charset=utf-8'
  }
});

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    // 从localStorage获取token
    const token = localStorage.getItem('access_token');
    
    // 如果token存在，添加到请求头
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // 打印请求日志（开发环境）
    if (import.meta.env.DEV) {
      console.log('🔄 请求:', config.method?.toUpperCase(), config.url);
      if (config.data) {
        console.log('📦 请求参数:', config.data);
      }
    }
    
    return config;
  },
  (error) => {
    console.error('❌ 请求错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
service.interceptors.response.use(
  (response) => {
    const res = response.data;
    
    // 打印响应日志（开发环境）
    if (import.meta.env.DEV) {
      console.log('✅ 响应:', response.config.url, res);
    }
    
    // 判断业务状态码
    if (res.code === 200) {
      return res;
    } else {
      // 业务错误
      ElMessage.error(res.message || '请求失败');
      return Promise.reject(new Error(res.message || '请求失败'));
    }
  },
  async (error) => {
    console.error('❌ 响应错误:', error);
    
    const originalRequest = error.config;
    
    // 处理401 Unauthorized
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // 尝试刷新token
        const refreshToken = localStorage.getItem('refresh_token');
        
        if (refreshToken) {
          const response = await axios.post(
            `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'}/auth/refresh`,
            { refresh_token: refreshToken }
          );
          
          const { access_token, refresh_token } = response.data.data;
          
          // 更新token
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', refresh_token);
          
          // 重试原请求
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return service(originalRequest);
        }
      } catch (refreshError) {
        // 刷新失败，清除token并跳转到登录页
        console.error('Token刷新失败:', refreshError);
        logout();
      }
    }
    
    // 处理其他错误
    let message = '网络错误，请稍后重试';
    
    if (error.response) {
      const { status, data } = error.response;
      
      switch (status) {
        case 400:
          message = data?.message || '请求参数错误';
          break;
        case 401:
          message = '登录已过期，请重新登录';
          logout();
          break;
        case 403:
          message = '没有权限执行此操作';
          break;
        case 404:
          message = '请求的资源不存在';
          break;
        case 500:
          message = data?.message || '服务器内部错误';
          break;
        default:
          message = data?.message || `请求失败 (${status})`;
      }
    } else if (error.request) {
      message = '网络连接失败，请检查网络';
    }
    
    ElMessage.error(message);
    return Promise.reject(error);
  }
);

// 退出登录
function logout() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user');
  localStorage.removeItem('permissions');
  localStorage.removeItem('roles');
  
  // 跳转到登录页
  if (router.currentRoute.value.path !== '/login') {
    router.push('/login');
  }
}

export default service;
```

### 环境变量配置

创建 `.env` 文件：

```env
# .env.development
VITE_API_BASE_URL=http://localhost:8000/api/v1

# .env.production
VITE_API_BASE_URL=https://api.example.com/api/v1
```

---

## 认证流程

### 完整认证流程说明

```
┌─────────┐                    ┌──────────┐                    ┌──────────┐
│  前端   │                    │  后端API │                    │  数据库  │
└────┬────┘                    └────┬─────┘                    └────┬─────┘
     │                               │                               │
     │  1. 发送登录请求              │                               │
     ├───────────────────────────────>                               │
     │  {username, password}        │                               │
     │                               │  2. 验证用户凭据               │
     │                               ├───────────────────────────────>
     │                               │                               │
     │                               │  3. 返回用户信息              │
     │                               <───────────────────────────────┤
     │                               │                               │
     │  4. 返回 access_token +     │                               │
     │     refresh_token + 用户信息 │                               │
     <───────────────────────────────┤                               │
     │                               │                               │
     │  5. 存储 tokens 和用户信息   │                               │
     │  (localStorage)              │                               │
     │                               │                               │
     │  6. 后续请求携带 token       │                               │
     ├───────────────────────────────>                               │
     │  Authorization: Bearer xxx   │                               │
     │                               │  7. 验证 token                │
     │                               │                               │
     │  8. 返回数据                 │                               │
     <───────────────────────────────┤                               │
     │                               │                               │
     │  9. Token 过期               │                               │
     <───────────────────────────────┤  401 Unauthorized            │
     │                               │                               │
     │  10. 使用 refresh_token      │                               │
     │      刷新 access_token       │                               │
     ├───────────────────────────────>                               │
     │  {refresh_token}             │                               │
     │                               │                               │
     │  11. 返回新 tokens           │                               │
     <───────────────────────────────┤                               │
     │                               │                               │
     │  12. 重试原请求              │                               │
     ├───────────────────────────────>                               │
     │  Authorization: Bearer new   │                               │
     │                               │                               │
```

### 登录功能实现

```javascript
// src/api/auth.js
import request from '@/utils/request';

// 登录
export function login(data) {
  return request({
    url: '/auth/login',
    method: 'post',
    data
  });
}

// 注册
export function register(data) {
  return request({
    url: '/auth/register',
    method: 'post',
    data
  });
}

// 刷新Token
export function refreshToken(data) {
  return request({
    url: '/auth/refresh',
    method: 'post',
    data
  });
}

// 修改密码
export function changePassword(data) {
  return request({
    url: '/auth/change-password',
    method: 'post',
    data
  });
}

// 重置密码
export function resetPassword(data) {
  return request({
    url: '/auth/reset-password',
    method: 'post',
    data
  });
}
```

### 登录页面示例 (Vue 3 + Element Plus)

```vue
<!-- src/views/Login.vue -->
<template>
  <div class="login-container">
    <div class="login-box">
      <h2>企业级RBAC系统</h2>
      
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        label-width="80px"
        @keyup.enter="handleLogin"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            style="width: 100%"
            @click="handleLogin"
          >
            {{ loading ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';
import { login } from '@/api/auth';
import { useUserStore } from '@/stores/user';

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

const loginFormRef = ref(null);
const loading = ref(false);

const loginForm = reactive({
  username: 'admin',
  password: 'password123'
});

const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ]
};

const handleLogin = async () => {
  if (!loginFormRef.value) return;
  
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true;
      
      try {
        const res = await login(loginForm);
        
        // 保存用户信息和token
        await userStore.login(res.data);
        
        ElMessage.success('登录成功');
        
        // 跳转到目标页面或首页
        const redirect = route.query.redirect || '/';
        router.push(redirect);
      } catch (error) {
        console.error('登录失败:', error);
      } finally {
        loading.value = false;
      }
    }
  });
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-box {
  width: 400px;
  padding: 40px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.login-box h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}
</style>
```

### 用户状态管理 (Pinia)

```javascript
// src/stores/user.js
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { login as loginApi, logout as logoutApi } from '@/api/auth';
import { getCurrentUserPermissions, getCurrentUserRoles } from '@/api/user';

export const useUserStore = defineStore('user', () => {
  // 状态
  const token = ref(localStorage.getItem('access_token') || '');
  const refreshToken = ref(localStorage.getItem('refresh_token') || '');
  const userInfo = ref(JSON.parse(localStorage.getItem('user') || 'null'));
  const permissions = ref(JSON.parse(localStorage.getItem('permissions') || '[]'));
  const roles = ref(JSON.parse(localStorage.getItem('roles') || '[]'));

  // 计算属性
  const isLoggedIn = computed(() => !!token.value && !!userInfo.value);
  const username = computed(() => userInfo.value?.username || '');
  const nickname = computed(() => userInfo.value?.nickname || '');
  const avatar = computed(() => userInfo.value?.avatar || '');

  // 登录
  async function login(data) {
    const { access_token, refresh_token, user } = data;
    
    token.value = access_token;
    refreshToken.value = refresh_token;
    userInfo.value = user;
    
    // 保存到localStorage
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    localStorage.setItem('user', JSON.stringify(user));
    
    // 获取用户权限和角色
    await fetchUserPermissions();
    await fetchUserRoles();
  }

  // 退出登录
  function logout() {
    token.value = '';
    refreshToken.value = '';
    userInfo.value = null;
    permissions.value = [];
    roles.value = [];
    
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    localStorage.removeItem('permissions');
    localStorage.removeItem('roles');
  }

  // 获取用户权限
  async function fetchUserPermissions() {
    try {
      const res = await getCurrentUserPermissions();
      permissions.value = res.data || [];
      localStorage.setItem('permissions', JSON.stringify(permissions.value));
    } catch (error) {
      console.error('获取权限失败:', error);
    }
  }

  // 获取用户角色
  async function fetchUserRoles() {
    try {
      const res = await getCurrentUserRoles();
      roles.value = res.data || [];
      localStorage.setItem('roles', JSON.stringify(roles.value));
    } catch (error) {
      console.error('获取角色失败:', error);
    }
  }

  // 检查是否有某个权限
  function hasPermission(permission) {
    if (!permission) return true;
    return permissions.value.includes(permission);
  }

  // 检查是否有某个角色
  function hasRole(role) {
    if (!role) return true;
    return roles.value.includes(role);
  }

  // 检查是否有任意一个权限
  function hasAnyPermission(permissionList) {
    if (!permissionList || permissionList.length === 0) return true;
    return permissionList.some(p => permissions.value.includes(p));
  }

  // 检查是否有任意一个角色
  function hasAnyRole(roleList) {
    if (!roleList || roleList.length === 0) return true;
    return roleList.some(r => roles.value.includes(r));
  }

  return {
    token,
    refreshToken,
    userInfo,
    permissions,
    roles,
    isLoggedIn,
    username,
    nickname,
    avatar,
    login,
    logout,
    fetchUserPermissions,
    fetchUserRoles,
    hasPermission,
    hasRole,
    hasAnyPermission,
    hasAnyRole
  };
});
```

---

## API请求封装

### 统一API模块结构

```javascript
// src/api/index.js - API统一出口
export * from './auth';
export * from './user';
export * from './role';
export * from './permission';
export * from './department';
export * from './menu';
export * from './system';
export * from './log';
```

### 用户管理API

```javascript
// src/api/user.js
import request from '@/utils/request';

// 获取用户列表
export function getUsers(params) {
  return request({
    url: '/users',
    method: 'get',
    params
  });
}

// 获取用户详情
export function getUserById(user_id) {
  return request({
    url: `/users/${user_id}`,
    method: 'get'
  });
}

// 创建用户
export function createUser(data) {
  return request({
    url: '/users',
    method: 'post',
    data
  });
}

// 更新用户
export function updateUser(user_id, data) {
  return request({
    url: `/users/${user_id}`,
    method: 'put',
    data
  });
}

// 删除用户
export function deleteUser(user_id) {
  return request({
    url: `/users/${user_id}`,
    method: 'delete'
  });
}

// 分配角色给用户
export function assignRolesToUser(user_id, role_ids) {
  return request({
    url: `/users/${user_id}/roles`,
    method: 'post',
    data: { role_ids }
  });
}

// 设置用户主角色
export function setPrimaryRole(user_id, role_id) {
  return request({
    url: `/users/${user_id}/primary-role`,
    method: 'post',
    data: { role_id }
  });
}

// 更新用户状态
export function updateUserStatus(user_id, status) {
  return request({
    url: `/users/${user_id}/status`,
    method: 'post',
    data: { status }
  });
}

// 获取当前用户权限
export function getCurrentUserPermissions() {
  return request({
    url: '/users/me/permissions',
    method: 'get'
  });
}

// 获取当前用户角色
export function getCurrentUserRoles() {
  return request({
    url: '/users/me/roles',
    method: 'get'
  });
}
```

### 角色管理API

```javascript
// src/api/role.js
import request from '@/utils/request';

// 获取角色列表
export function getRoles(params) {
  return request({
    url: '/roles',
    method: 'get',
    params
  });
}

// 获取所有启用的角色
export function getAllActiveRoles() {
  return request({
    url: '/roles/all',
    method: 'get'
  });
}

// 获取角色详情
export function getRoleById(role_id) {
  return request({
    url: `/roles/${role_id}`,
    method: 'get'
  });
}

// 创建角色
export function createRole(data) {
  return request({
    url: '/roles',
    method: 'post',
    data
  });
}

// 更新角色
export function updateRole(role_id, data) {
  return request({
    url: `/roles/${role_id}`,
    method: 'put',
    data
  });
}

// 删除角色
export function deleteRole(role_id) {
  return request({
    url: `/roles/${role_id}`,
    method: 'delete'
  });
}

// 分配权限给角色
export function assignPermissionsToRole(role_id, permission_ids) {
  return request({
    url: `/roles/${role_id}/permissions`,
    method: 'post',
    data: { permission_ids }
  });
}

// 更新角色状态
export function updateRoleStatus(role_id, status) {
  return request({
    url: `/roles/${role_id}/status`,
    method: 'post',
    data: { status }
  });
}
```

### 权限管理API

```javascript
// src/api/permission.js
import request from '@/utils/request';

// 获取权限列表
export function getPermissions(params) {
  return request({
    url: '/permissions',
    method: 'get',
    params
  });
}

// 获取所有启用的权限
export function getAllActivePermissions() {
  return request({
    url: '/permissions/all',
    method: 'get'
  });
}

// 获取权限树形结构
export function getPermissionTree() {
  return request({
    url: '/permissions/tree',
    method: 'get'
  });
}

// 获取权限详情
export function getPermissionById(permission_id) {
  return request({
    url: `/permissions/${permission_id}`,
    method: 'get'
  });
}

// 创建权限
export function createPermission(data) {
  return request({
    url: '/permissions',
    method: 'post',
    data
  });
}

// 更新权限
export function updatePermission(permission_id, data) {
  return request({
    url: `/permissions/${permission_id}`,
    method: 'put',
    data
  });
}

// 删除权限
export function deletePermission(permission_id) {
  return request({
    url: `/permissions/${permission_id}`,
    method: 'delete'
  });
}
```

### 部门管理API

```javascript
// src/api/department.js
import request from '@/utils/request';

// 获取部门列表
export function getDepartments(params) {
  return request({
    url: '/departments',
    method: 'get',
    params
  });
}

// 获取部门树形结构
export function getDepartmentTree() {
  return request({
    url: '/departments/tree',
    method: 'get'
  });
}

// 获取部门详情
export function getDepartmentById(department_id) {
  return request({
    url: `/departments/${department_id}`,
    method: 'get'
  });
}

// 创建部门
export function createDepartment(data) {
  return request({
    url: '/departments',
    method: 'post',
    data
  });
}

// 更新部门
export function updateDepartment(department_id, data) {
  return request({
    url: `/departments/${department_id}`,
    method: 'put',
    data
  });
}

// 删除部门
export function deleteDepartment(department_id) {
  return request({
    url: `/departments/${department_id}`,
    method: 'delete'
  });
}
```

---

## 各模块接口调用示例

### 用户管理页面示例

```vue
<!-- src/views/system/UserManagement.vue -->
<template>
  <div class="user-management">
    <!-- 搜索区域 -->
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="关键词">
          <el-input
            v-model="searchForm.keyword"
            placeholder="用户名/昵称/邮箱"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        
        <el-form-item label="部门">
          <el-tree-select
            v-model="searchForm.department_id"
            :data="departmentTree"
            :props="{ label: 'name', value: 'id', children: 'children' }"
            placeholder="请选择部门"
            clearable
            check-strictly
          />
        </el-form-item>
        
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择" clearable>
            <el-option label="启用" :value="1" />
            <el-option label="禁用" :value="0" />
          </el-select>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon> 搜索
          </el-button>
          <el-button @click="handleReset">
            <el-icon><Refresh /></el-icon> 重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 操作按钮 -->
    <el-card class="table-card">
      <template #header>
        <div class="card-header">
          <span>用户列表</span>
          <el-button type="primary" @click="handleAdd" v-permission="'user:create'">
            <el-icon><Plus /></el-icon> 新增用户
          </el-button>
        </div>
      </template>

      <!-- 表格 -->
      <el-table :data="tableData" border v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" width="120" />
        <el-table-column prop="nickname" label="昵称" width="120" />
        <el-table-column prop="email" label="邮箱" width="180" />
        <el-table-column prop="phone" label="手机号" width="130" />
        <el-table-column prop="department_name" label="部门" width="120" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'danger'">
              {{ row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="last_login_time" label="最后登录" width="170" />
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="handleView(row)" v-permission="'user:view'">
              查看
            </el-button>
            <el-button link type="primary" size="small" @click="handleEdit(row)" v-permission="'user:update'">
              编辑
            </el-button>
            <el-button link type="primary" size="small" @click="handleAssignRoles(row)" v-permission="'user:update'">
              分配角色
            </el-button>
            <el-button link type="danger" size="small" @click="handleDelete(row)" v-permission="'user:delete'">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.page_size"
        :total="pagination.total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        style="margin-top: 20px; justify-content: flex-end"
      />
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新增用户' : '编辑用户'"
      width="600px"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" :disabled="dialogType === 'edit'" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="dialogType === 'add'">
          <el-input v-model="form.password" type="password" show-password />
        </el-form-item>
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="form.nickname" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="部门" prop="department_id">
          <el-tree-select
            v-model="form.department_id"
            :data="departmentTree"
            :props="{ label: 'name', value: 'id', children: 'children' }"
            placeholder="请选择部门"
            check-strictly
          />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio :value="1">启用</el-radio>
            <el-radio :value="0">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmit">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 分配角色对话框 -->
    <el-dialog v-model="assignRolesVisible" title="分配角色" width="500px">
      <el-checkbox-group v-model="selectedRoleIds">
        <el-checkbox
          v-for="role in allRoles"
          :key="role.id"
          :label="role.id"
        >
          {{ role.name }}
        </el-checkbox>
      </el-checkbox-group>
      
      <template #footer>
        <el-button @click="assignRolesVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmitAssignRoles">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Search, Refresh, Plus } from '@element-plus/icons-vue';
import {
  getUsers,
  getUserById,
  createUser,
  updateUser,
  deleteUser,
  assignRolesToUser
} from '@/api/user';
import { getAllActiveRoles } from '@/api/role';
import { getDepartmentTree } from '@/api/department';

// 搜索表单
const searchForm = reactive({
  keyword: '',
  department_id: null,
  status: null
});

// 分页
const pagination = reactive({
  page: 1,
  page_size: 10,
  total: 0
});

// 表格数据
const tableData = ref([]);
const loading = ref(false);

// 对话框
const dialogVisible = ref(false);
const dialogType = ref('add');
const submitLoading = ref(false);
const formRef = ref(null);

const form = reactive({
  id: null,
  username: '',
  password: '',
  nickname: '',
  email: '',
  phone: '',
  department_id: null,
  status: 1
});

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  nickname: [{ required: true, message: '请输入昵称', trigger: 'blur' }]
};

// 分配角色
const assignRolesVisible = ref(false);
const selectedRoleIds = ref([]);
const allRoles = ref([]);
const currentUserId = ref(null);

// 部门树
const departmentTree = ref([]);

// 获取数据
const fetchData = async () => {
  loading.value = true;
  try {
    const res = await getUsers({
      ...searchForm,
      page: pagination.page,
      page_size: pagination.page_size
    });
    
    tableData.value = res.data || [];
    pagination.total = res.total || 0;
  } catch (error) {
    console.error('获取用户列表失败:', error);
  } finally {
    loading.value = false;
  }
};

// 获取部门树
const fetchDepartmentTree = async () => {
  try {
    const res = await getDepartmentTree();
    departmentTree.value = res.data || [];
  } catch (error) {
    console.error('获取部门树失败:', error);
  }
};

// 获取所有角色
const fetchAllRoles = async () => {
  try {
    const res = await getAllActiveRoles();
    allRoles.value = res.data || [];
  } catch (error) {
    console.error('获取角色列表失败:', error);
  }
};

// 搜索
const handleSearch = () => {
  pagination.page = 1;
  fetchData();
};

// 重置
const handleReset = () => {
  searchForm.keyword = '';
  searchForm.department_id = null;
  searchForm.status = null;
  pagination.page = 1;
  fetchData();
};

// 新增
const handleAdd = () => {
  dialogType.value = 'add';
  Object.assign(form, {
    id: null,
    username: '',
    password: '',
    nickname: '',
    email: '',
    phone: '',
    department_id: null,
    status: 1
  });
  dialogVisible.value = true;
};

// 查看
const handleView = async (row) => {
  try {
    const res = await getUserById(row.id);
    console.log('用户详情:', res.data);
  } catch (error) {
    console.error('获取用户详情失败:', error);
  }
};

// 编辑
const handleEdit = async (row) => {
  dialogType.value = 'edit';
  try {
    const res = await getUserById(row.id);
    Object.assign(form, res.data);
    dialogVisible.value = true;
  } catch (error) {
    console.error('获取用户详情失败:', error);
  }
};

// 提交
const handleSubmit = async () => {
  if (!formRef.value) return;
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitLoading.value = true;
      
      try {
        if (dialogType.value === 'add') {
          await createUser(form);
          ElMessage.success('创建成功');
        } else {
          await updateUser(form.id, form);
          ElMessage.success('更新成功');
        }
        
        dialogVisible.value = false;
        fetchData();
      } catch (error) {
        console.error('提交失败:', error);
      } finally {
        submitLoading.value = false;
      }
    }
  });
};

// 删除
const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该用户吗？', '提示', {
    type: 'warning'
  }).then(async () => {
    try {
      await deleteUser(row.id);
      ElMessage.success('删除成功');
      fetchData();
    } catch (error) {
      console.error('删除失败:', error);
    }
  }).catch(() => {});
};

// 分配角色
const handleAssignRoles = async (row) => {
  currentUserId.value = row.id;
  
  try {
    const res = await getUserById(row.id);
    const userRoles = res.data.roles || [];
    selectedRoleIds.value = userRoles.map(r => r.id);
  } catch (error) {
    selectedRoleIds.value = [];
  }
  
  assignRolesVisible.value = true;
};

// 提交分配角色
const handleSubmitAssignRoles = async () => {
  try {
    await assignRolesToUser(currentUserId.value, selectedRoleIds.value);
    ElMessage.success('分配成功');
    assignRolesVisible.value = false;
    fetchData();
  } catch (error) {
    console.error('分配角色失败:', error);
  }
};

// 分页变化
const handleSizeChange = (size) => {
  pagination.page_size = size;
  pagination.page = 1;
  fetchData();
};

const handleCurrentChange = (page) => {
  pagination.page = page;
  fetchData();
};

onMounted(() => {
  fetchData();
  fetchDepartmentTree();
  fetchAllRoles();
});
</script>

<style scoped>
.user-management {
  padding: 20px;
}

.search-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
```

---

## 状态管理方案

### Pinia Store 完整示例

```javascript
// src/stores/index.js
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

export default pinia;
```

```javascript
// src/stores/app.js - 应用全局状态
import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useAppStore = defineStore('app', () => {
  const sidebarCollapsed = ref(false);
  const device = ref('desktop');
  const theme = ref('light');

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value;
  }

  function setDevice(val) {
    device.value = val;
  }

  function setTheme(val) {
    theme.value = val;
  }

  return {
    sidebarCollapsed,
    device,
    theme,
    toggleSidebar,
    setDevice,
    setTheme
  };
}, {
  persist: {
    key: 'app-settings',
    storage: localStorage,
    paths: ['theme', 'sidebarCollapsed']
  }
});
```

```javascript
// src/stores/permission.js - 权限和菜单状态
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { getCurrentUserMenuTree } from '@/api/menu';

export const usePermissionStore = defineStore('permission', () => {
  const menuTree = ref([]);
  const loading = ref(false);

  const flattenMenus = computed(() => {
    const result = [];
    const flatten = (menus) => {
      menus.forEach(menu => {
        result.push(menu);
        if (menu.children && menu.children.length > 0) {
          flatten(menu.children);
        }
      });
    };
    flatten(menuTree.value);
    return result;
  });

  async function fetchMenuTree() {
    loading.value = true;
    try {
      const res = await getCurrentUserMenuTree();
      menuTree.value = res.data || [];
    } catch (error) {
      console.error('获取菜单失败:', error);
    } finally {
      loading.value = false;
    }
  }

  function reset() {
    menuTree.value = [];
  }

  return {
    menuTree,
    flattenMenus,
    loading,
    fetchMenuTree,
    reset
  };
});
```

---

## 路由守卫

### Vue Router 配置

```javascript
// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { usePermissionStore } from '@/stores/permission';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'Layout',
    component: () => import('@/layout/index.vue'),
    redirect: '/dashboard',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { title: '仪表盘', requiresAuth: true }
      },
      {
        path: 'system',
        name: 'System',
        redirect: '/system/user',
        meta: { title: '系统管理', requiresAuth: true },
        children: [
          {
            path: 'user',
            name: 'UserManagement',
            component: () => import('@/views/system/UserManagement.vue'),
            meta: { title: '用户管理', requiresAuth: true, permission: 'user:view' }
          },
          {
            path: 'role',
            name: 'RoleManagement',
            component: () => import('@/views/system/RoleManagement.vue'),
            meta: { title: '角色管理', requiresAuth: true, permission: 'role:view' }
          },
          {
            path: 'permission',
            name: 'PermissionManagement',
            component: () => import('@/views/system/PermissionManagement.vue'),
            meta: { title: '权限管理', requiresAuth: true, permission: 'permission:view' }
          },
          {
            path: 'department',
            name: 'DepartmentManagement',
            component: () => import('@/views/system/DepartmentManagement.vue'),
            meta: { title: '部门管理', requiresAuth: true, permission: 'department:view' }
          },
          {
            path: 'menu',
            name: 'MenuManagement',
            component: () => import('@/views/system/MenuManagement.vue'),
            meta: { title: '菜单管理', requiresAuth: true, permission: 'menu:view' }
          }
        ]
      },
      {
        path: 'log',
        name: 'Log',
        redirect: '/log/operation',
        meta: { title: '日志管理', requiresAuth: true },
        children: [
          {
            path: 'operation',
            name: 'OperationLog',
            component: () => import('@/views/log/OperationLog.vue'),
            meta: { title: '操作日志', requiresAuth: true, permission: 'log:view' }
          },
          {
            path: 'audit',
            name: 'AuditLog',
            component: () => import('@/views/log/AuditLog.vue'),
            meta: { title: '审计日志', requiresAuth: true, permission: 'audit:view' }
          }
        ]
      }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// 全局前置守卫
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore();
  const permissionStore = usePermissionStore();

  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 企业级RBAC系统`;
  }

  // 检查是否需要认证
  if (to.meta.requiresAuth !== false) {
    // 需要认证
    if (!userStore.isLoggedIn) {
      // 未登录，跳转到登录页
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      });
      return;
    }

    // 检查权限
    if (to.meta.permission) {
      if (!userStore.hasPermission(to.meta.permission)) {
        ElMessage.error('没有权限访问该页面');
        next(from.path || '/');
        return;
      }
    }

    // 如果没有菜单数据，获取菜单
    if (permissionStore.menuTree.length === 0) {
      await permissionStore.fetchMenuTree();
    }
  } else {
    // 不需要认证
    if (to.path === '/login' && userStore.isLoggedIn) {
      // 已登录，跳转到首页
      next('/');
      return;
    }
  }

  next();
});

export default router;
```

---

## 错误处理

### 全局错误处理

```javascript
// src/utils/errorHandler.js
import { ElMessage, ElNotification } from 'element-plus';

// 错误类型
export const ErrorTypes = {
  NETWORK_ERROR: 'NETWORK_ERROR',
  AUTH_ERROR: 'AUTH_ERROR',
  PERMISSION_ERROR: 'PERMISSION_ERROR',
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  SERVER_ERROR: 'SERVER_ERROR',
  UNKNOWN_ERROR: 'UNKNOWN_ERROR'
};

// 错误处理
export function handleError(error, options = {}) {
  const {
    showMessage = true,
    showNotification = false,
    logError = true
  } = options;

  let errorType = ErrorTypes.UNKNOWN_ERROR;
  let errorMessage = '发生未知错误';

  if (error.response) {
    const { status, data } = error.response;
    
    switch (status) {
      case 400:
        errorType = ErrorTypes.VALIDATION_ERROR;
        errorMessage = data?.message || '请求参数错误';
        break;
      case 401:
        errorType = ErrorTypes.AUTH_ERROR;
        errorMessage = data?.message || '登录已过期';
        break;
      case 403:
        errorType = ErrorTypes.PERMISSION_ERROR;
        errorMessage = data?.message || '没有权限';
        break;
      case 404:
        errorMessage = data?.message || '资源不存在';
        break;
      case 409:
        errorMessage = data?.message || '数据已存在';
        break;
      case 422:
        errorType = ErrorTypes.VALIDATION_ERROR;
        errorMessage = data?.message || '数据验证失败';
        break;
      case 500:
        errorType = ErrorTypes.SERVER_ERROR;
        errorMessage = data?.message || '服务器内部错误';
        break;
      default:
        errorMessage = data?.message || `请求失败 (${status})`;
    }
  } else if (error.request) {
    errorType = ErrorTypes.NETWORK_ERROR;
    errorMessage = '网络连接失败，请检查网络';
  } else {
    errorMessage = error.message || '发生未知错误';
  }

  // 记录错误日志
  if (logError) {
    console.error('❌ 错误详情:', {
      type: errorType,
      message: errorMessage,
      originalError: error
    });
  }

  // 显示消息
  if (showMessage) {
    const messageType = errorType === ErrorTypes.AUTH_ERROR ? 'warning' : 'error';
    ElMessage[messageType](errorMessage);
  }

  // 显示通知
  if (showNotification) {
    ElNotification.error({
      title: '错误',
      message: errorMessage,
      duration: 4500
    });
  }

  return {
    type: errorType,
    message: errorMessage
  };
}

// 异步错误捕获
export function asyncErrorHandler(fn, options = {}) {
  return async (...args) => {
    try {
      return await fn(...args);
    } catch (error) {
      handleError(error, options);
      throw error;
    }
  };
}
```

---

## 权限控制

### 权限指令

```javascript
// src/directives/permission.js
import { useUserStore } from '@/stores/user';

export default {
  mounted(el, binding) {
    const { value } = binding;
    const userStore = useUserStore();
    
    if (value && typeof value === 'string') {
      if (!userStore.hasPermission(value)) {
        el.parentNode && el.parentNode.removeChild(el);
      }
    } else if (value && Array.isArray(value)) {
      if (!userStore.hasAnyPermission(value)) {
        el.parentNode && el.parentNode.removeChild(el);
      }
    }
  }
};
```

### 角色指令

```javascript
// src/directives/role.js
import { useUserStore } from '@/stores/user';

export default {
  mounted(el, binding) {
    const { value } = binding;
    const userStore = useUserStore();
    
    if (value && typeof value === 'string') {
      if (!userStore.hasRole(value)) {
        el.parentNode && el.parentNode.removeChild(el);
      }
    } else if (value && Array.isArray(value)) {
      if (!userStore.hasAnyRole(value)) {
        el.parentNode && el.parentNode.removeChild(el);
      }
    }
  }
};
```

### 注册指令

```javascript
// src/directives/index.js
import permission from './permission';
import role from './role';

export function setupDirectives(app) {
  app.directive('permission', permission);
  app.directive('role', role);
}
```

### 权限组件

```vue
<!-- src/components/PermissionWrapper.vue -->
<template>
  <slot v-if="hasPermission" />
</template>

<script setup>
import { computed } from 'vue';
import { useUserStore } from '@/stores/user';

const props = defineProps({
  permission: {
    type: [String, Array],
    default: ''
  }
});

const userStore = useUserStore();

const hasPermission = computed(() => {
  if (!props.permission) return true;
  
  if (typeof props.permission === 'string') {
    return userStore.hasPermission(props.permission);
  }
  
  if (Array.isArray(props.permission)) {
    return userStore.hasAnyPermission(props.permission);
  }
  
  return true;
});
</script>
```

---

## 常见组件封装

### 分页表格组件

```vue
<!-- src/components/PageTable.vue -->
<template>
  <div class="page-table">
    <el-table :data="data" v-loading="loading" border stripe>
      <slot></slot>
    </el-table>
    
    <el-pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :total="total"
      :page-sizes="[10, 20, 50, 100]"
      layout="total, sizes, prev, pager, next, jumper"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      style="margin-top: 20px; justify-content: flex-end"
    />
  </div>
</template>

<script setup>
const props = defineProps({
  data: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  total: {
    type: Number,
    default: 0
  },
  page: {
    type: Number,
    default: 1
  },
  pageSize: {
    type: Number,
    default: 10
  }
});

const emit = defineEmits(['update:page', 'update:pageSize', 'change']);

const currentPage = computed({
  get: () => props.page,
  set: (val) => emit('update:page', val)
});

const pageSizeVal = computed({
  get: () => props.pageSize,
  set: (val) => emit('update:pageSize', val)
});

const handleSizeChange = (size) => {
  pageSizeVal.value = size;
  currentPage.value = 1;
  emit('change', { page: 1, pageSize: size });
};

const handleCurrentChange = (page) => {
  currentPage.value = page;
  emit('change', { page, pageSize: pageSizeVal.value });
};
</script>
```

### 搜索表单组件

```vue
<!-- src/components/SearchForm.vue -->
<template>
  <el-card class="search-form">
    <el-form :inline="true" :model="form">
      <slot></slot>
      <el-form-item>
        <el-button type="primary" @click="handleSearch">
          <el-icon><Search /></el-icon> 搜索
        </el-button>
        <el-button @click="handleReset">
          <el-icon><Refresh /></el-icon> 重置
        </el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup>
import { Search, Refresh } from '@element-plus/icons-vue';

const props = defineProps({
  form: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['search', 'reset']);

const handleSearch = () => {
  emit('search');
};

const handleReset = () => {
  emit('reset');
};
</script>

<style scoped>
.search-form {
  margin-bottom: 20px;
}
</style>
```

### 确认对话框 Hook

```javascript
// src/hooks/useConfirm.js
import { ElMessageBox } from 'element-plus';

export function useConfirm() {
  const confirm = (message, title = '提示', options = {}) => {
    return ElMessageBox.confirm(message, title, {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
      ...options
    });
  };

  const confirmDelete = (message = '确定要删除吗？') => {
    return confirm(message, '删除确认');
  };

  return {
    confirm,
    confirmDelete
  };
}
```

### 表格操作 Hook

```javascript
// src/hooks/useTable.js
import { ref, reactive } from 'vue';

export function useTable(fetchFn) {
  const data = ref([]);
  const loading = ref(false);
  const pagination = reactive({
    page: 1,
    pageSize: 10,
    total: 0
  });

  const fetchData = async (params = {}) => {
    loading.value = true;
    try {
      const res = await fetchFn({
        page: pagination.page,
        pageSize: pagination.pageSize,
        ...params
      });
      data.value = res.data || [];
      pagination.total = res.total || 0;
    } catch (error) {
      console.error('获取数据失败:', error);
    } finally {
      loading.value = false;
    }
  };

  const handlePageChange = (page) => {
    pagination.page = page;
    fetchData();
  };

  const handleSizeChange = (size) => {
    pagination.pageSize = size;
    pagination.page = 1;
    fetchData();
  };

  const refresh = () => {
    fetchData();
  };

  return {
    data,
    loading,
    pagination,
    fetchData,
    handlePageChange,
    handleSizeChange,
    refresh
  };
}
```

---

## 最佳实践

### 1. 文件结构规范

```
src/
├── api/              # API接口层
├── assets/           # 静态资源
├── components/       # 公共组件
├── directives/       # 自定义指令
├── hooks/            # 组合式函数
├── layout/           # 布局组件
├── router/           # 路由配置
├── stores/           # 状态管理
├── utils/            # 工具函数
├── views/            # 页面组件
├── App.vue
└── main.js
```

### 2. 命名规范

- **组件文件**：大驼峰 (PascalCase) - `UserManagement.vue`
- **普通文件**：小驼峰 (camelCase) 或 下划线 (snake_case) - `userApi.js`, `user_api.js`
- **常量**：大写 + 下划线 - `MAX_PAGE_SIZE`
- **私有函数**：下划线前缀 - `_internalMethod`

### 3. 组件编写规范

```vue
<template>
  <div class="component-name">
    <!-- 模板内容 -->
  </div>
</template>

<script setup>
// 1. 导入
import { ref, computed, onMounted } from 'vue';
import { useStore } from '@/stores';

// 2. Props定义
const props = defineProps({
  // ...
});

// 3. Emits定义
const emit = defineEmits(['change', 'update']);

// 4. 响应式数据
const state = ref('');

// 5. 计算属性
const computedValue = computed(() => {
  // ...
});

// 6. 方法
const handleClick = () => {
  // ...
};

// 7. 生命周期
onMounted(() => {
  // ...
});
</script>

<style scoped>
.component-name {
  // 样式
}
</style>
```

### 4. API调用规范

```javascript
// ✅ 推荐
try {
  const res = await getUserList(params);
  // 处理成功
} catch (error) {
  // 错误已在拦截器中处理
}

// ❌ 避免
getUserList(params).then(res => {
  // ...
}).catch(err => {
  // 重复处理错误
});
```

### 5. 性能优化

- 使用 `v-memo` 优化列表渲染
- 合理使用 `computed` 缓存计算结果
- 路由懒加载
- 组件按需引入
- 使用虚拟滚动处理大数据列表

---

## 常见问题

### Q1: 如何处理Token过期？

A: Token过期已在axios响应拦截器中自动处理，会尝试使用refresh_token刷新token。如果刷新失败，会自动跳转到登录页。

### Q2: 如何实现权限控制？

A: 三种方式：
1. 路由守卫：在路由meta中配置permission
2. 权限指令：`v-permission="'user:view'"`
3. 权限组件：`<PermissionWrapper permission="user:view">`

### Q3: 如何处理分页？

A: 使用 `useTable` Hook 或 `PageTable` 组件，统一处理分页逻辑。

### Q4: 如何添加新的API模块？

A: 
1. 在 `src/api/` 下创建新文件
2. 定义API函数
3. 在 `src/api/index.js` 中导出
4. 在页面中导入使用

### Q5: 如何调试API请求？

A: 
1. 打开浏览器开发者工具 Network 面板
2. 查看请求/响应详情
3. 开发环境会在控制台打印请求日志

### Q6: 跨域问题如何解决？

A: 
1. 后端配置CORS（已配置）
2. 开发环境使用vite代理：
```javascript
// vite.config.js
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

---

## 附录

### A. 快速参考

| 功能 | 文件位置 |
|------|----------|
| API请求封装 | `src/utils/request.js` |
| 用户Store | `src/stores/user.js` |
| 路由配置 | `src/router/index.js` |
| 权限指令 | `src/directives/permission.js` |

### B. 相关文档

- [用户文档](./User_Guide.md)
- [API参考文档](./API_Reference.md)
- [后端开发指南](./Backend_Development_Guide.md)

---

**文档版本**: v1.0.0
**最后更新**: 2026-04-11
