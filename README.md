# 企业级RBAC系统

基于 FastAPI 构建的企业级 RBAC（基于角色的访问控制）权限管理系统。

## 目录

- [项目简介](#项目简介)
- [技术栈](#技术栈)
- [系统架构](#系统架构)
- [功能特性](#功能特性)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [配置说明](#配置说明)
- [API文档](#api文档)
- [开发指南](#开发指南)
- [常见问题](#常见问题)

## 项目简介

企业级RBAC系统是一个功能完善、安全可靠的权限管理平台，采用基于角色的访问控制模型，为企业应用提供统一的用户、角色、权限、部门、菜单等管理功能。

### 核心设计理念

- **安全性优先**: 采用JWT认证、密码加密、访问日志等多重安全机制
- **高可扩展性**: 模块化设计，支持租户隔离、数据权限等高级特性
- **易于维护**: 清晰的代码结构和完善的文档
- **高性能**: Redis缓存、数据库索引优化等性能提升措施

## 技术栈

### 核心框架

- **FastAPI**: 现代化、高性能的Web框架，支持异步处理
- **Uvicorn**: ASGI服务器，用于运行FastAPI应用

### 数据库与ORM

- **SQLAlchemy**: Python SQL工具包和对象关系映射
- **Alembic**: 数据库迁移工具
- **PyMySQL**: MySQL数据库驱动

### 认证与安全

- **python-jose**: JWT (JSON Web Token) 编码/解码库
- **Passlib**: 密码哈希库，支持BCrypt
- **cryptography**: 加密工具库

### 数据验证

- **Pydantic**: 数据验证和设置管理
- **pydantic-settings**: 基于Pydantic的应用配置管理

### 缓存

- **Redis**: 内存数据存储，用于缓存和会话管理

### 测试与代码质量

- **pytest**: 测试框架
- **pytest-asyncio**: 异步测试支持
- **httpx**: HTTP客户端，用于API测试
- **black**: 代码格式化
- **flake8**: 代码检查
- **isort**: 导入排序
- **mypy**: 类型检查

### 工具库

- **python-dotenv**: 环境变量管理
- **python-multipart**: 文件上传支持

## 系统架构

### 分层架构

```
┌─────────────────────────────────────────────────────────────┐
│                        API 层 (App/Api/)                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Auth      │  │   Users     │  │   Roles     │  ...    │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      依赖注入层 (App/Dependencies/)            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │    Auth     │  │  Database   │  │  Permission  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      仓储层 (App/Repositories/)               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ UserRepo    │  │ RoleRepo    │  │ PermRepo    │  ...    │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      数据模型层 (App/Models/)                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ UserModel   │  │ RoleModel   │  │ PermModel   │  ...    │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        数据库层 (MySQL/Redis)                   │
└─────────────────────────────────────────────────────────────┘
```

### 核心模块说明

#### 1. API 层 (App/Api/)

- 定义RESTful API端点
- 请求/响应验证
- 路由注册和版本管理
- 支持API版本控制（V1）

#### 2. 核心层 (App/Core/)

- **Database.py**: 数据库连接和会话管理
- **Exceptions.py**: 自定义异常类
- **Middleware.py**: 中间件（CORS、认证、日志）
- **Security.py**: 安全相关工具
- **Decorators.py**: 装饰器

#### 3. 依赖注入层 (App/Dependencies/)

- **Auth.py**: 认证依赖，获取当前用户
- **Database.py**: 数据库会话依赖
- **Permission.py**: 权限检查依赖

#### 4. 模型层 (App/Models/)

- 定义数据库表结构
- 关系映射
- 基础模型包含通用字段（租户ID、创建时间、更新时间、删除标记等）

#### 5. 仓储层 (App/Repositories/)

- 封装数据库操作
- 提供CRUD基础方法
- 实现业务查询逻辑

#### 6. 模式层 (App/Schemas/)

- Pydantic模型定义
- 请求/响应数据验证
- 数据序列化

#### 7. 配置层 (App/Config/)

- **Settings.py**: 应用配置管理
- **Database.py**: 数据库配置
- **Security.py**: 安全配置
- **CacheKeys.py**: 缓存键定义

## 功能特性

### 用户管理

- 用户CRUD操作
- 用户状态管理（启用/禁用）
- 用户密码重置
- 用户头像上传
- 用户资料管理
- 用户与角色关联
- 用户与用户组关联
- 用户登录记录

### 角色管理

- 角色CRUD操作
- 角色层级管理（支持父角色）
- 角色类型（系统角色、功能角色、数据角色、自定义角色）
- 角色数据范围配置
- 角色与权限关联
- 角色状态管理

### 权限管理

- 权限CRUD操作
- 权限类型（菜单权限、按钮权限、API权限）
- 权限层级结构
- 权限编码唯一标识

### 部门管理

- 部门CRUD操作
- 部门层级结构（树形结构）
- 部门与用户关联
- 部门状态管理

### 菜单管理

- 菜单CRUD操作
- 菜单层级结构
- 菜单类型（目录、菜单、按钮）
- 菜单图标、路由、组件配置
- 菜单与权限关联
- 菜单排序

### 用户组管理

- 用户组CRUD操作
- 用户组成员管理
- 用户组与角色关联
- 用户组数据权限

### 数据权限规则

- 数据权限规则CRUD
- 规则条件配置
- 规则与角色、用户组关联
- 动态数据过滤

### 系统字典

- 字典类型管理
- 字典项管理
- 字典排序
- 系统常量配置

### 系统配置

- 系统参数配置
- 配置项分组
- 配置值类型支持

### 日志管理

- 操作日志记录
- 审计日志记录
- 日志查询和过滤
- 日志导出

### 用户会话管理

- 在线用户查看
- 会话强制下线
- 会话超时管理

### 监控指标

- 系统健康检查
- 性能指标统计
- 用户活跃度统计

### 安全特性

- JWT Token认证
- Access Token + Refresh Token双Token机制
- 密码BCrypt加密
- 请求签名验证
- IP白名单/黑名单
- 操作日志审计
- 数据防篡改（乐观锁）
- 软删除机制

### 多租户支持

- 租户隔离
- 租户数据安全
- 租户级配置

## 项目结构

```
enterprise-rbac-system/
├── App/
│   ├── Api/                    # API层
│   │   ├── V1/                 # API V1版本
│   │   │   ├── Auth.py         # 认证API
│   │   │   ├── Users.py        # 用户API
│   │   │   ├── Roles.py        # 角色API
│   │   │   ├── Permissions.py  # 权限API
│   │   │   ├── Departments.py  # 部门API
│   │   │   ├── Menus.py        # 菜单API
│   │   │   ├── UserGroups.py   # 用户组API
│   │   │   ├── DataPermissionRules.py  # 数据权限API
│   │   │   ├── SystemDicts.py  # 系统字典API
│   │   │   ├── SystemConfigs.py # 系统配置API
│   │   │   ├── OperationLogs.py # 操作日志API
│   │   │   ├── AuditLogs.py    # 审计日志API
│   │   │   ├── UserSessions.py # 用户会话API
│   │   │   ├── UserProfiles.py # 用户资料API
│   │   │   ├── Metrics.py      # 监控指标API
│   │   │   ├── Health.py       # 健康检查API
│   │   │   └── __init__.py
│   │   └── Routers.py          # 路由注册
│   ├── Config/                  # 配置层
│   │   ├── Settings.py         # 应用配置
│   │   ├── Database.py         # 数据库配置
│   │   ├── Security.py         # 安全配置
│   │   └── CacheKeys.py        # 缓存键
│   ├── Core/                    # 核心层
│   │   ├── Database.py         # 数据库连接
│   │   ├── Exceptions.py       # 自定义异常
│   │   ├── Middleware.py       # 中间件
│   │   ├── Security.py         # 安全工具
│   │   ├── Decorators.py       # 装饰器
│   │   └── __init__.py
│   ├── Dependencies/            # 依赖注入
│   │   ├── Auth.py             # 认证依赖
│   │   ├── Database.py         # 数据库依赖
│   │   ├── Permission.py       # 权限依赖
│   │   └── __init__.py
│   ├── Models/                  # 数据模型
│   │   ├── Base.py             # 基础模型
│   │   ├── User.py             # 用户模型
│   │   ├── Role.py             # 角色模型
│   │   ├── Permission.py       # 权限模型
│   │   ├── Department.py       # 部门模型
│   │   ├── Menu.py             # 菜单模型
│   │   ├── UserGroup.py        # 用户组模型
│   │   ├── DataPermissionRule.py  # 数据权限规则模型
│   │   ├── SystemDict.py       # 系统字典模型
│   │   ├── SystemConfig.py     # 系统配置模型
│   │   ├── OperationLog.py     # 操作日志模型
│   │   ├── AuditLog.py         # 审计日志模型
│   │   ├── UserSession.py      # 用户会话模型
│   │   ├── UserProfile.py      # 用户资料模型
│   │   ├── UserRole.py         # 用户角色关系模型
│   │   ├── RolePermission.py   # 角色权限关系模型
│   │   ├── MenuPermission.py   # 菜单权限关系模型
│   │   ├── UserGroupRelation.py # 用户组关系模型
│   │   ├── UserGroupRoleRelation.py # 用户组角色关系模型
│   │   └── __init__.py
│   ├── Repositories/            # 仓储层
│   │   ├── Base.py             # 基础仓储
│   │   ├── UserRepository.py   # 用户仓储
│   │   ├── RoleRepository.py   # 角色仓储
│   │   ├── PermissionRepository.py  # 权限仓储
│   │   ├── DepartmentRepository.py  # 部门仓储
│   │   ├── MenuRepository.py   # 菜单仓储
│   │   ├── ...                 # 其他仓储
│   │   └── __init__.py
│   ├── Schemas/                 # 模式层
│   │   ├── Base.py             # 基础模式
│   │   ├── Auth.py             # 认证模式
│   │   ├── User.py             # 用户模式
│   │   ├── Role.py             # 角色模式
│   │   ├── ...                 # 其他模式
│   │   └── __init__.py
│   ├── Utils/                   # 工具类
│   │   ├── Logger.py           # 日志工具
│   │   ├── Response.py         # 响应工具
│   │   ├── CacheWarmup.py      # 缓存预热
│   │   └── ...
│   └── Main.py                  # 应用入口
├── Logs/                        # 日志目录
├── uploads/                     # 上传文件目录
├── .env                         # 环境变量（不提交）
├── .env.example                 # 环境变量示例
├── .gitignore                   # Git忽略文件
├── requirements.txt             # Python依赖
└── README.md                    # 项目文档
```

## 快速开始

### 环境要求

- Python 3.12+
- MySQL 8.0+
- Redis 6.0+

### 1. 克隆项目

```bash
git clone 
cd enterprise-rbac-system
```

### 2. 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置数据库、Redis等连接信息：

```env
# 数据库配置
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/rbac_db?charset=utf8mb4

# JWT配置
JWT_SECRET_KEY=your-secret-key-here-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Redis配置
REDIS_URL=redis://127.0.0.1:6379/0

# 应用配置
APP_NAME=Enterprise RBAC System
APP_VERSION=1.0.0
APP_DEBUG=False

# 安全配置
PASSWORD_SALT_LENGTH=16
BCRYPT_ROUNDS=12

# 上传配置
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=5242880
ALLOWED_IMAGE_EXTENSIONS=png,jpg,jpeg,gif

# CORS配置
CORS_ORIGINS=http://127.0.0.1:3000,http://127.0.0.1:8080

# 日志配置
LOG_LEVEL=INFO
LOG_DIR=./Logs
```

### 5. 创建数据库

```sql
CREATE DATABASE rbac_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. 数据库迁移

使用 Alembic 进行数据库迁移：

```bash
# 初始化迁移（如果尚未初始化）
alembic init alembic

# 创建迁移脚本
alembic revision --autogenerate -m "init"

# 执行迁移
alembic upgrade head
-----------------------------------------------------------------------------
#也可以参考

```

或者直接使用 SQLAlchemy 创建表（开发环境）：

```python
from App.Config.Database import engine
from App.Models.Base import Base

Base.metadata.create_all(bind=engine)
```

### 7. 初始化数据

创建初始管理员用户和基础数据。

### 8. 启动应用

```bash
# 开发模式（自动重载）
python -m App.Main

# 或使用 uvicorn 直接运行
uvicorn App.Main:app --reload --host 0.0.0.0 --port 8000
```

### 9. 访问应用

- 应用地址: <http://localhost:8000>
- API文档 (Swagger): <http://localhost:8000/docs>
- API文档 (ReDoc): <http://localhost:8000/redoc>
- OpenAPI Schema: <http://localhost:8000/openapi.json>

## 配置说明

### 数据库配置

`DATABASE_URL` 格式：

```
mysql+pymysql://<user>:<password>@<host>:<port>/<database>?charset=utf8mb4
```

### JWT配置

- `JWT_SECRET_KEY`: JWT签名密钥，生产环境必须使用强随机密钥
- `JWT_ALGORITHM`: 签名算法，默认 HS256
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`: Access Token过期时间（分钟）
- `JWT_REFRESH_TOKEN_EXPIRE_DAYS`: Refresh Token过期时间（天）

### Redis配置

- `REDIS_URL`: Redis连接URL
- `REDIS_SENTINEL_URLS`: Redis Sentinel地址（可选）
- `REDIS_SENTINEL_MASTER_NAME`: Redis Sentinel主节点名称（可选）

### 安全配置

- `PASSWORD_SALT_LENGTH`: 密码盐长度
- `BCRYPT_ROUNDS`: BCrypt加密轮数，越高越安全但越慢

### 上传配置

- `UPLOAD_DIR`: 上传文件保存目录
- `MAX_FILE_SIZE`: 最大文件大小（字节），默认5MB
- `ALLOWED_IMAGE_EXTENSIONS`: 允许的图片扩展名

### CORS配置

- `CORS_ORIGINS`: 允许的跨域来源，多个来源用逗号分隔

### 日志配置

- `LOG_LEVEL`: 日志级别（DEBUG、INFO、WARNING、ERROR、CRITICAL）
- `LOG_DIR`: 日志文件保存目录

## API文档

### 认证流程

1. **用户登录**
   ```
   POST /api/v1/auth/login
   Body: { username, password }
   Response: { access_token, refresh_token, user_info }
   ```
2. **使用Access Token**
   在请求头中添加：
   ```
   Authorization: Bearer <access_token>
   ```
3. **刷新Token**
   ```
   POST /api/v1/auth/refresh
   Body: { refresh_token }
   Response: { access_token }
   ```
4. **用户登出**
   ```
   POST /api/v1/auth/logout
   ```

### API端点概览

| 模块   | 端点前缀                          | 说明              |
| ---- | ----------------------------- | --------------- |
| 认证   | /api/v1/auth                  | 用户登录、登出、Token刷新 |
| 用户   | /api/v1/users                 | 用户CRUD、状态管理     |
| 角色   | /api/v1/roles                 | 角色CRUD、权限分配     |
| 权限   | /api/v1/permissions           | 权限CRUD          |
| 部门   | /api/v1/departments           | 部门CRUD、树形结构     |
| 菜单   | /api/v1/menus                 | 菜单CRUD、树形结构     |
| 用户组  | /api/v1/user-groups           | 用户组CRUD、成员管理    |
| 数据权限 | /api/v1/data-permission-rules | 数据权限规则          |
| 系统字典 | /api/v1/system-dicts          | 字典管理            |
| 系统配置 | /api/v1/system-configs        | 配置管理            |
| 操作日志 | /api/v1/operation-logs        | 操作日志查询          |
| 审计日志 | /api/v1/audit-logs            | 审计日志查询          |
| 用户会话 | /api/v1/user-sessions         | 会话管理            |
| 用户资料 | /api/v1/user-profiles         | 资料管理            |
| 监控   | /api/v1/metrics               | 系统指标            |
| 健康检查 | /api/v1/health                | 健康检查            |

### 统一响应格式

所有API响应遵循统一格式：

**成功响应：**

```json
{
  "code": 200,
  "message": "操作成功",
  "data": { ... }
}
```

**失败响应：**

```json
{
  "code": 400,
  "message": "错误信息",
  "error_code": 40001,
  "data": null
}
```

### 分页查询

列表查询支持分页参数：

```
GET /api/v1/users?page=1&page_size=20&keyword=admin
```

响应：

```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "items": [...],
    "total": 100,
    "page": 1,
    "page_size": 20,
    "total_pages": 5
  }
}
```

## 开发指南

### 代码规范

项目使用以下工具保证代码质量：

- **black**: 代码格式化
- **flake8**: 代码检查
- **isort**: 导入排序
- **mypy**: 类型检查

运行代码检查：

```bash
# 格式化代码
black .

# 检查代码
flake8 .

# 排序导入
isort .

# 类型检查
mypy .
```

### 新增API模块

1. **创建数据模型** (`App/Models/YourModel.py`)
2. **创建Schema** (`App/Schemas/YourModel.py`)
3. **创建Repository** (`App/Repositories/YourModelRepository.py`)
4. **创建API路由** (`App/Api/V1/YourModel.py`)
5. **注册路由** (`App/Api/V1/__init__.py`)

### 数据库迁移

```bash
# 创建新的迁移
alembic revision --autogenerate -m "description"

# 应用迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1

# 查看迁移历史
alembic history
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_auth.py

# 显示详细输出
pytest -v

# 生成覆盖率报告
pytest --cov=App --cov-report=html
```

## 常见问题

### 1. 数据库连接失败

检查 `.env` 中的 `DATABASE_URL` 配置是否正确，确保MySQL服务已启动。

### 2. Redis连接失败

检查Redis服务是否启动，`REDIS_URL` 配置是否正确。

### 3. JWT Token过期

使用Refresh Token获取新的Access Token，或重新登录。

### 4. 权限不足

确保当前用户拥有相应的角色和权限，检查角色权限配置。

### 5. 上传文件失败

检查 `UPLOAD_DIR` 目录是否存在且有写入权限，文件大小是否超过限制。

## 许可证

[MIT License](LICENSE)

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

- 项目地址: \[GitHub Repository]
- 问题反馈: \[Issue Tracker]

