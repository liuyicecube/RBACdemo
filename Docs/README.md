# 企业级RBAC系统 - 文档索引

## 📚 文档概览

本目录包含企业级RBAC系统的完整文档集合。

***

## 📖 文档列表

### 1. 用户文档 (`User_Guide.md`)

**面向人群**：系统用户、前端开发人员

**内容概要**：

- 系统概述和快速开始指南
- 用户、角色、权限、部门等功能的使用说明
- API基础路径和认证方式介绍
- 常见问题解答

**快速链接**：[User\_Guide.md](./User_Guide.md)

***

### 2. API参考文档 (`API_Reference.md`)

**面向人群**：前端开发人员、API集成开发人员

**内容概要**：

- 所有API接口的详细说明
- 请求/响应参数、示例代码
- 错误码说明
- 认证方式详解

**包含接口**：

- ✅ 认证接口 (登录、注册、Token刷新等)
- ✅ 用户管理接口 (CRUD、角色分配等)
- ✅ 角色管理接口 (CRUD、权限分配等)
- ✅ 权限管理接口 (CRUD、树形结构等)
- ✅ 部门管理接口 (CRUD、树形结构等)
- ✅ 菜单管理接口
- ✅ 系统字典接口
- ✅ 系统配置接口
- ✅ 操作日志接口
- ✅ 审计日志接口
- ✅ 用户组接口
- ✅ 数据权限规则接口
- ✅ 用户会话接口
- ✅ 用户资料接口
- ✅ 系统监控接口

**快速链接**：[API\_Reference.md](./API_Reference.md)

***

### 3. 前端开发师文档 (`Frontend_Development_Guide.md`)

**面向人群**：前端开发人员

**内容概要**：

- 快速开始和环境准备
- 完整的API基础配置
- 认证流程实现（登录、Token管理）
- API请求封装（Axios配置、拦截器）
- 各模块接口调用示例（用户管理、角色管理等）
- 状态管理方案（Pinia）
- 路由守卫实现
- 错误处理机制
- 权限控制（指令、组件）
- 常见组件封装
- 最佳实践和常见问题

**包含内容**：

- ✅ Axios完整配置和拦截器
- ✅ 登录页面完整示例
- ✅ 用户状态管理（Pinia Store）
- ✅ 用户管理页面完整示例
- ✅ 权限指令和权限组件
- ✅ 分页表格、搜索表单等公共组件
- ✅ 常用Hooks（useTable、useConfirm等）

**快速链接**：[Frontend\_Development\_Guide.md](./Frontend_Development_Guide.md)

***

### 4. 后端开发师文档 (`Backend_Development_Guide.md`)

**面向人群**：后端开发人员、系统架构师

**内容概要**：

- 技术架构和项目结构详解
- 核心模块设计说明
- 数据库设计文档
- 完整的开发指南
- 新增API开发流程（6步走）
- 测试和部署指南
- 最佳实践和常见问题

**包含章节**：

- 项目概述和核心特性
- 技术架构图和分层说明
- 完整目录结构
- 核心模块详解（Auth、Users、Roles、Permissions等）
- 数据库设计（8个核心数据表）
- 环境搭建和开发流程
- 测试指南
- 部署指南（Gunicorn、Docker、Docker Compose）
- 最佳实践（代码规范、数据库操作、错误处理等）

**快速链接**：[Backend\_Development\_Guide.md](./Backend_Development_Guide.md)

***

## 🚀 快速开始

### 如果你是系统用户

1. 阅读 [User\_Guide.md](./User_Guide.md) 了解系统功能
2. 查看 [API\_Reference.md](./API_Reference.md) 了解如何调用API

### 如果你是前端开发人员

1. 阅读 [Frontend\_Development\_Guide.md](./Frontend_Development_Guide.md) 了解完整的前端集成方案
2. 参考 [API\_Reference.md](./API_Reference.md) 了解所有接口细节
3. 参考 [User\_Guide.md](./User_Guide.md) 了解业务逻辑

### 如果你是后端开发人员

1. 阅读 [Backend\_Development\_Guide.md](./Backend_Development_Guide.md) 了解完整技术架构
2. 按照"新增API开发流程"进行新功能开发
3. 参考 [API\_Reference.md](./API_Reference.md) 了解现有接口

***

## 🎯 系统特性

企业级RBAC系统核心功能：

- 🔐 完整的RBAC权限模型
- 🏢 多租户支持
- 🔑 JWT认证机制
- 📊 数据权限控制
- 📝 操作日志审计
- 📈 系统监控指标
- 📚 完整的API文档
- ✅ 单元测试和集成测试

