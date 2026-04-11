# 企业级RBAC系统 - 后端开发师功能文档

## 目录
- [项目概述](#项目概述)
- [技术架构](#技术架构)
- [项目结构](#项目结构)
- [核心模块详解](#核心模块详解)
- [数据库设计](#数据库设计)
- [开发指南](#开发指南)
- [测试指南](#测试指南)
- [部署指南](#部署指南)
- [最佳实践](#最佳实践)
- [常见问题](#常见问题)

---

## 项目概述

### 项目简介

企业级RBAC（基于角色的访问控制）系统是一个完整的用户权限管理解决方案，采用现代化的FastAPI框架构建，提供企业级的用户、角色、权限、部门等核心功能管理。

### 核心特性

- ✅ 完整的RBAC权限模型
- ✅ 多租户支持
- ✅ JWT认证机制
- ✅ 数据权限控制
- ✅ 操作日志审计
- ✅ 系统监控指标
- ✅ 完整的API文档
- ✅ 单元测试和集成测试

### 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Python | 3.12+ | 编程语言 |
| FastAPI | 最新 | Web框架 |
| SQLAlchemy | 最新 | ORM框架 |
| Pydantic | 最新 | 数据验证 |
| PyMySQL | 最新 | MySQL驱动 |
| Redis | 最新 | 缓存/会话 |
| JWT | - | 认证令牌 |
| Uvicorn | 最新 | ASGI服务器 |

---

## 技术架构

### 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                         客户端层                          │
│  (Web前端 / 移动应用 / 第三方系统)                       │
└────────────────────────────┬────────────────────────────┘
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────┐
│                      API网关层 (FastAPI)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  CORS中间件  │  │  认证中间件  │  │  日志中间件  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│                      路由层 (Routers)                      │
│  /api/v1/auth, /api/v1/users, /api/v1/roles, ...      │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│                     服务层 (Services)                      │
│  AuthService, UserService, RoleService, ...             │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│                   数据访问层 (Repositories)                │
│  UserRepository, RoleRepository, PermissionRepository   │
└────────────────────────────┬────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   MySQL       │    │    Redis      │    │  文件存储     │
│  主数据库     │    │   缓存/会话   │    │   (上传)      │
└───────────────┘    └───────────────┘    └───────────────┘
```

### 分层架构说明

#### 1. API层 (Routers)
- 职责：定义API接口、请求验证、响应格式化
- 位置：`App/Api/V1/`
- 文件命名：`{Module}.py` (如 `Users.py`, `Roles.py`)

#### 2. 服务层 (Services)
- 职责：业务逻辑处理、事务管理、权限校验
- 位置：`App/Services/`
- 文件命名：`{Module}Service.py` (如 `UserService.py`)

#### 3. 数据访问层 (Repositories)
- 职责：数据库CRUD操作、查询构建
- 位置：`App/Repositories/`
- 文件命名：`{Module}Repository.py`

#### 4. 模型层 (Models)
- 职责：数据库表定义、关系映射
- 位置：`App/Models/`
- 文件命名：`{Module}.py`

#### 5. 数据传输层 (Schemas)
- 职责：请求/响应数据验证、序列化
- 位置：`App/Schemas/`
- 文件命名：`{Module}.py`

---

## 项目结构

### 完整目录结构

```
enterprise-rbac-system/
├── App/
│   ├── Api/
│   │   ├── Routers.py              # 路由注册
│   │   └── V1/                     # API V1版本
│   │       ├── __init__.py         # V1路由聚合
│   │       ├── Auth.py             # 认证接口
│   │       ├── Users.py            # 用户管理接口
│   │       ├── Roles.py            # 角色管理接口
│   │       ├── Permissions.py      # 权限管理接口
│   │       ├── Departments.py      # 部门管理接口
│   │       ├── Menus.py            # 菜单管理接口
│   │       ├── Metrics.py          # 系统监控接口
│   │       ├── SystemDicts.py      # 系统字典接口
│   │       ├── SystemConfigs.py    # 系统配置接口
│   │       ├── OperationLogs.py    # 操作日志接口
│   │       ├── AuditLogs.py        # 审计日志接口
│   │       ├── UserGroups.py       # 用户组接口
│   │       ├── DataPermissionRules.py # 数据权限规则接口
│   │       ├── UserSessions.py     # 用户会话接口
│   │       └── UserProfiles.py     # 用户资料接口
│   ├── Config/
│   │   ├── Settings.py             # 应用配置
│   │   ├── Database.py             # 数据库配置
│   │   ├── Security.py             # 安全配置
│   │   └── CacheKeys.py            # 缓存Key定义
│   ├── Core/
│   │   ├── Database.py             # 数据库连接
│   │   ├── Exceptions.py           # 自定义异常
│   │   ├── Middleware.py           # 中间件
│   │   └── Security.py             # 安全工具
│   ├── Dependencies/
│   │   ├── Database.py             # 数据库依赖
│   │   ├── Auth.py                 # 认证依赖
│   │   └── Permission.py           # 权限依赖
│   ├── Models/
│   │   ├── Base.py                 # 基础模型
│   │   ├── User.py                 # 用户模型
│   │   ├── Role.py                 # 角色模型
│   │   ├── Permission.py           # 权限模型
│   │   ├── Department.py           # 部门模型
│   │   ├── Menu.py                 # 菜单模型
│   │   ├── UserRole.py             # 用户角色关系
│   │   ├── RolePermission.py       # 角色权限关系
│   │   ├── OperationLog.py         # 操作日志
│   │   ├── AuditLog.py             # 审计日志
│   │   └── ...                     # 其他模型
│   ├── Repositories/
│   │   ├── Base.py                 # 基础仓库
│   │   ├── UserRepository.py       # 用户仓库
│   │   ├── RoleRepository.py       # 角色仓库
│   │   ├── PermissionRepository.py # 权限仓库
│   │   └── ...                     # 其他仓库
│   ├── Schemas/
│   │   ├── Base.py                 # 基础Schema
│   │   ├── Auth.py                 # 认证Schema
│   │   ├── User.py                 # 用户Schema
│   │   ├── Role.py                 # 角色Schema
│   │   ├── Permission.py           # 权限Schema
│   │   └── ...                     # 其他Schema
│   ├── Services/
│   │   ├── AuthService.py          # 认证服务
│   │   ├── UserService.py          # 用户服务
│   │   ├── RoleService.py          # 角色服务
│   │   ├── PermissionService.py    # 权限服务
│   │   └── ...                     # 其他服务
│   ├── Utils/
│   │   ├── Logger.py               # 日志工具
│   │   ├── Response.py             # 响应工具
│   │   ├── Cache.py                # 缓存工具
│   │   └── ...                     # 其他工具
│   └── Main.py                     # 应用入口
├── Tests/
│   ├── test_enterprise_monitoring.py # 监控测试
│   ├── test_round18_demo.py        # 演示测试
│   └── test_documentation.md       # 测试文档
├── Docs/
│   ├── User_Guide.md               # 用户文档
│   ├── API_Reference.md            # API文档
│   └── Backend_Development_Guide.md # 本文件
├── Logs/                            # 日志目录
├── Uploads/                         # 上传文件目录
├── .env                             # 环境变量
├── .env.example                     # 环境变量示例
├── requirements.txt                 # Python依赖
└── README.md                        # 项目说明
```

---

## 核心模块详解

### 1. 认证模块 (Auth)

#### 核心类

**AuthService** - 认证服务

```python
from App.Services.AuthService import AuthService

auth_service = AuthService(db_session)

# 用户登录
login_result = auth_service.login(username="admin", password="password", ip="127.0.0.1")

# 用户注册
user = auth_service.register(
    username="newuser",
    password="password",
    nickname="新用户",
    tenant_id=1
)

# 刷新Token
new_tokens = auth_service.refresh_token(refresh_token="xxx")

# 修改密码
auth_service.change_password(user_id=1, old_password="old", new_password="new")
```

#### JWT Token结构

**Access Token** (短期，默认30分钟)
```python
{
  "sub": "user_id",
  "username": "admin",
  "type": "access",
  "exp": 1234567890
}
```

**Refresh Token** (长期，默认7天)
```python
{
  "sub": "user_id",
  "type": "refresh",
  "exp": 1234567890
}
```

---

### 2. 用户模块 (Users)

#### 核心类

**UserService** - 用户服务

```python
from App.Services.UserService import UserService

user_service = UserService(db_session)

# 分页查询
total, users = user_service.paginate_users(
    tenant_id=1,
    keyword="admin",
    department_id=1,
    status=1,
    page=1,
    page_size=10
)

# 获取用户
user = user_service.get_user_by_id(user_id=1, tenant_id=1)

# 创建用户
user = user_service.create_user(
    tenant_id=1,
    username="newuser",
    password="password",
    nickname="新用户"
)

# 更新用户
user = user_service.update_user(user_id=1, tenant_id=1, data={...})

# 删除用户
user_service.delete_user(user_id=1, tenant_id=1)

# 分配角色
user_service.assign_roles(user_id=1, tenant_id=1, role_ids=[1, 2, 3])
```

---

### 3. 角色模块 (Roles)

#### 核心类

**RoleService** - 角色服务

```python
from App.Services.RoleService import RoleService

role_service = RoleService(db_session)

# 分页查询
total, roles = role_service.paginate_roles(
    tenant_id=1,
    keyword="admin",
    status=1,
    page=1,
    page_size=10
)

# 获取所有启用角色
roles = role_service.get_all_active_roles(tenant_id=1)

# 创建角色
role = role_service.create_role(
    tenant_id=1,
    name="新角色",
    code="new_role",
    description="描述"
)

# 分配权限
role_service.assign_permissions(role_id=1, tenant_id=1, permission_ids=[1, 2, 3])
```

---

### 4. 权限模块 (Permissions)

#### 核心类

**PermissionService** - 权限服务

```python
from App.Services.PermissionService import PermissionService

permission_service = PermissionService(db_session)

# 分页查询
total, permissions = permission_service.paginate_permissions(
    tenant_id=1,
    keyword="user",
    permission_type=1,
    status=1,
    page=1,
    page_size=10
)

# 获取所有启用权限
permissions = permission_service.get_all_active_permissions(tenant_id=1)

# 权限编码规范
# 格式: {resource}:{action}
# 示例: user:view, user:create, role:update
```

---

### 5. 依赖注入模块

#### 数据库依赖

```python
from App.Dependencies.Database import get_db

# 在路由中使用
@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    pass
```

#### 认证依赖

```python
from App.Dependencies.Auth import get_current_user, get_current_user_and_tenant_id

# 获取当前用户
@router.get("/profile")
def get_profile(current_user: UserModel = Depends(get_current_user)):
    pass

# 获取当前用户和租户ID
@router.get("/users")
def get_users(
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
):
    current_user, tenant_id = current_user_with_tenant
    pass
```

#### 权限依赖

```python
from App.Dependencies.Permission import permission_dependency

# 使用权限依赖
@router.get("/users", dependencies=[Depends(permission_dependency("user:view"))])
def get_users():
    pass
```

---

## 数据库设计

### 核心数据表

#### 1. 用户表 (sys_user)

| 字段 | 类型 | 说明 | 索引 |
|------|------|------|------|
| id | INT | 主键 | PK |
| tenant_id | INT | 租户ID | IDX |
| username | VARCHAR(50) | 用户名 | UNIQUE |
| password | VARCHAR(255) | 密码哈希 | - |
| nickname | VARCHAR(50) | 昵称 | - |
| email | VARCHAR(100) | 邮箱 | IDX |
| phone | VARCHAR(20) | 手机号 | IDX |
| avatar | VARCHAR(255) | 头像 | - |
| department_id | INT | 部门ID | FK, IDX |
| status | INT | 状态 | IDX |
| last_login_time | DATETIME | 最后登录时间 | - |
| last_login_ip | VARCHAR(50) | 最后登录IP | - |
| create_time | DATETIME | 创建时间 | - |
| update_time | DATETIME | 更新时间 | - |

#### 2. 角色表 (sys_role)

| 字段 | 类型 | 说明 | 索引 |
|------|------|------|------|
| id | INT | 主键 | PK |
| tenant_id | INT | 租户ID | IDX |
| name | VARCHAR(50) | 角色名称 | - |
| code | VARCHAR(50) | 角色编码 | UNIQUE |
| description | TEXT | 描述 | - |
| sort | INT | 排序 | - |
| status | INT | 状态 | IDX |
| create_time | DATETIME | 创建时间 | - |
| update_time | DATETIME | 更新时间 | - |

#### 3. 权限表 (sys_permission)

| 字段 | 类型 | 说明 | 索引 |
|------|------|------|------|
| id | INT | 主键 | PK |
| tenant_id | INT | 租户ID | IDX |
| name | VARCHAR(50) | 权限名称 | - |
| code | VARCHAR(100) | 权限编码 | UNIQUE |
| type | INT | 权限类型 | - |
| resource_type | VARCHAR(50) | 资源类型 | - |
| resource_id | INT | 资源ID | - |
| action | VARCHAR(50) | 操作类型 | - |
| path | VARCHAR(255) | API路径 | - |
| method | VARCHAR(10) | HTTP方法 | - |
| parent_id | INT | 父权限ID | FK |
| level | INT | 层级 | - |
| status | INT | 状态 | IDX |
| create_time | DATETIME | 创建时间 | - |
| update_time | DATETIME | 更新时间 | - |

#### 4. 用户角色关系表 (sys_user_role)

| 字段 | 类型 | 说明 | 索引 |
|------|------|------|------|
| id | INT | 主键 | PK |
| user_id | INT | 用户ID | FK, IDX |
| role_id | INT | 角色ID | FK, IDX |
| is_primary | BOOLEAN | 是否主角色 | - |
| create_time | DATETIME | 创建时间 | - |

#### 5. 角色权限关系表 (sys_role_permission)

| 字段 | 类型 | 说明 | 索引 |
|------|------|------|------|
| id | INT | 主键 | PK |
| role_id | INT | 角色ID | FK, IDX |
| permission_id | INT | 权限ID | FK, IDX |
| create_time | DATETIME | 创建时间 | - |

#### 6. 部门表 (sys_department)

| 字段 | 类型 | 说明 | 索引 |
|------|------|------|------|
| id | INT | 主键 | PK |
| tenant_id | INT | 租户ID | IDX |
| name | VARCHAR(50) | 部门名称 | - |
| code | VARCHAR(50) | 部门编码 | UNIQUE |
| parent_id | INT | 父部门ID | FK |
| level | INT | 层级 | - |
| description | TEXT | 描述 | - |
| status | INT | 状态 | IDX |
| create_time | DATETIME | 创建时间 | - |
| update_time | DATETIME | 更新时间 | - |

#### 7. 操作日志表 (sys_operation_log)

| 字段 | 类型 | 说明 | 索引 |
|------|------|------|------|
| id | INT | 主键 | PK |
| tenant_id | INT | 租户ID | IDX |
| user_id | INT | 用户ID | FK, IDX |
| module | VARCHAR(50) | 模块 | IDX |
| operation | VARCHAR(50) | 操作 | IDX |
| method | VARCHAR(10) | 请求方法 | - |
| url | VARCHAR(255) | 请求URL | - |
| params | TEXT | 请求参数 | - |
| result | TEXT | 响应结果 | - |
| ip | VARCHAR(50) | IP地址 | - |
| duration | INT | 耗时(ms) | - |
| status | INT | 状态 | - |
| error_message | TEXT | 错误信息 | - |
| create_time | DATETIME | 创建时间 | IDX |

#### 8. 审计日志表 (sys_audit_log)

| 字段 | 类型 | 说明 | 索引 |
|------|------|------|------|
| id | INT | 主键 | PK |
| tenant_id | INT | 租户ID | IDX |
| user_id | INT | 用户ID | FK, IDX |
| action | VARCHAR(50) | 操作类型 | IDX |
| resource_type | VARCHAR(50) | 资源类型 | - |
| resource_id | INT | 资源ID | - |
| old_value | TEXT | 旧值 | - |
| new_value | TEXT | 新值 | - |
| ip | VARCHAR(50) | IP地址 | - |
| create_time | DATETIME | 创建时间 | IDX |

---

## 开发指南

### 环境搭建

#### 1. 克隆项目

```bash
git clone <repository-url>
cd enterprise-rbac-system
```

#### 2. 创建虚拟环境

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 3. 安装依赖

```bash
pip install -r requirements.txt
```

#### 4. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```env
# 应用配置
APP_NAME=Enterprise RBAC System
APP_VERSION=1.0.0
APP_DEBUG=True

# 数据库配置
DATABASE_URL=mysql+pymysql://user:password@host:3306/dbname?charset=utf8mb4

# JWT配置
JWT_SECRET_KEY=your-secret-key-here-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Redis配置
REDIS_URL=redis://localhost:6379/0

# CORS配置
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# 日志配置
LOG_LEVEL=INFO
LOG_DIR=./Logs
```

#### 5. 启动应用

```bash
# 开发模式（自动重载）
python App/Main.py

# 或使用uvicorn直接启动
uvicorn App.Main:app --reload --host 0.0.0.0 --port 8000
```

#### 6. 访问API文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

### 新增API开发流程

#### 步骤1：创建Schema

文件：`App/Schemas/Example.py`

```python
from pydantic import BaseModel, Field
from typing import Optional
from App.Schemas.Base import BaseResponse


class ExampleCreate(BaseModel):
    """创建示例请求"""
    name: str = Field(..., description="名称", min_length=1, max_length=50)
    code: str = Field(..., description="编码", min_length=1, max_length=50)
    description: Optional[str] = Field(None, description="描述")


class ExampleUpdate(BaseModel):
    """更新示例请求"""
    name: Optional[str] = Field(None, description="名称")
    description: Optional[str] = Field(None, description="描述")


class ExampleResponse(BaseModel):
    """示例响应"""
    id: int
    name: str
    code: str
    description: Optional[str]
    status: int
    create_time: str
    update_time: str
```

#### 步骤2：创建Model

文件：`App/Models/Example.py`

```python
from sqlalchemy import Column, String, Integer, Text, Index
from App.Models.Base import BaseModel


class ExampleModel(BaseModel):
    """示例模型"""
    
    __tablename__ = "sys_example"
    __table_args__ = (
        Index('idx_example_status', 'status'),
    )
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    tenant_id = Column(Integer, nullable=False, index=True, comment="租户ID")
    name = Column(String(50), nullable=False, comment="名称")
    code = Column(String(50), nullable=False, unique=True, comment="编码")
    description = Column(Text, nullable=True, comment="描述")
    status = Column(Integer, default=1, comment="状态(0:禁用,1:启用)")
```

#### 步骤3：创建Repository

文件：`App/Repositories/ExampleRepository.py`

```python
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from App.Repositories.Base import BaseRepository
from App.Models.Example import ExampleModel


class ExampleRepository(BaseRepository[ExampleModel]):
    """示例仓库"""
    
    def __init__(self, db: Session):
        super().__init__(db, ExampleModel)
    
    def paginate_examples(
        self,
        tenant_id: int,
        keyword: Optional[str] = None,
        status: Optional[int] = None,
        page: int = 1,
        page_size: int = 10
    ) -> Tuple[int, List[ExampleModel]]:
        """分页查询示例"""
        query = self.db.query(ExampleModel).filter(
            ExampleModel.tenant_id == tenant_id
        )
        
        if keyword:
            query = query.filter(
                or_(
                    ExampleModel.name.contains(keyword),
                    ExampleModel.code.contains(keyword)
                )
            )
        
        if status is not None:
            query = query.filter(ExampleModel.status == status)
        
        total = query.count()
        offset = (page - 1) * page_size
        examples = query.offset(offset).limit(page_size).all()
        
        return total, examples
    
    def get_by_code(self, code: str, tenant_id: int) -> Optional[ExampleModel]:
        """根据编码获取"""
        return self.db.query(ExampleModel).filter(
            and_(
                ExampleModel.code == code,
                ExampleModel.tenant_id == tenant_id
            )
        ).first()
```

#### 步骤4：创建Service

文件：`App/Services/ExampleService.py`

```python
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException
from App.Repositories.ExampleRepository import ExampleRepository
from App.Models.Example import ExampleModel
from App.Schemas.Example import ExampleCreate, ExampleUpdate


class ExampleService:
    """示例服务"""
    
    def __init__(self, db: Session):
        self.db = db
        self.example_repo = ExampleRepository(db)
    
    def paginate_examples(
        self,
        tenant_id: int,
        keyword: Optional[str] = None,
        status: Optional[int] = None,
        page: int = 1,
        page_size: int = 10
    ) -> Tuple[int, List[ExampleModel]]:
        """分页查询示例"""
        return self.example_repo.paginate_examples(
            tenant_id=tenant_id,
            keyword=keyword,
            status=status,
            page=page,
            page_size=page_size
        )
    
    def get_example_by_id(self, example_id: int, tenant_id: int) -> ExampleModel:
        """根据ID获取示例"""
        example = self.example_repo.get_by_id_and_tenant(example_id, tenant_id)
        if not example:
            raise HTTPException(status_code=404, detail="示例不存在")
        return example
    
    def create_example(self, tenant_id: int, data: ExampleCreate) -> ExampleModel:
        """创建示例"""
        # 检查编码是否已存在
        existing = self.example_repo.get_by_code(data.code, tenant_id)
        if existing:
            raise HTTPException(status_code=400, detail="编码已存在")
        
        example = ExampleModel(
            tenant_id=tenant_id,
            name=data.name,
            code=data.code,
            description=data.description,
            status=1
        )
        
        return self.example_repo.create(example)
    
    def update_example(
        self,
        example_id: int,
        tenant_id: int,
        data: ExampleUpdate
    ) -> ExampleModel:
        """更新示例"""
        example = self.get_example_by_id(example_id, tenant_id)
        
        update_data = data.model_dump(exclude_unset=True)
        return self.example_repo.update(example, update_data)
    
    def delete_example(self, example_id: int, tenant_id: int) -> None:
        """删除示例"""
        example = self.get_example_by_id(example_id, tenant_id)
        self.example_repo.delete(example)
```

#### 步骤5：创建Router

文件：`App/Api/V1/Examples.py`

```python
"""Example Management API"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from App.Schemas.Example import ExampleCreate, ExampleUpdate
from App.Schemas.Auth import AuthResponse
from App.Services.ExampleService import ExampleService
from App.Dependencies.Database import get_db
from App.Dependencies.Auth import get_current_user_and_tenant_id
from App.Dependencies.Permission import permission_dependency
from App.Utils.Response import ResponseUtils


router = APIRouter(
    prefix="/examples",
    tags=["示例管理"]
)


@router.get("", response_model=AuthResponse, summary="获取示例列表", dependencies=[Depends(permission_dependency("example:view"))])
def get_examples(
    keyword: str = None,
    status: int = None,
    page: int = 1,
    page_size: int = 10,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取示例列表接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        example_service = ExampleService(db)
        
        total, examples = example_service.paginate_examples(
            tenant_id=tenant_id,
            keyword=keyword,
            status=status,
            page=page,
            page_size=page_size
        )
        
        example_list = []
        for example in examples:
            example_list.append({
                "id": example.id,
                "name": example.name,
                "code": example.code,
                "description": example.description,
                "status": example.status,
                "create_time": example.create_time.isoformat() if hasattr(example.create_time, 'isoformat') else example.create_time,
                "update_time": example.update_time.isoformat() if hasattr(example.update_time, 'isoformat') else example.update_time
            })
        
        return ResponseUtils.pagination(
            data=example_list,
            total=total,
            page=page,
            page_size=page_size,
            message="获取示例列表成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_examples: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get("/{example_id}", response_model=AuthResponse, summary="获取示例详情", dependencies=[Depends(permission_dependency("example:view"))])
def get_example(
    example_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取示例详情接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        example_service = ExampleService(db)
        example = example_service.get_example_by_id(example_id, tenant_id)
        
        return ResponseUtils.success(data={
            "id": example.id,
            "name": example.name,
            "code": example.code,
            "description": example.description,
            "status": example.status,
            "create_time": example.create_time.isoformat() if hasattr(example.create_time, 'isoformat') else example.create_time,
            "update_time": example.update_time.isoformat() if hasattr(example.update_time, 'isoformat') else example.update_time
        }, message="获取示例详情成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.post("", response_model=AuthResponse, summary="创建示例", dependencies=[Depends(permission_dependency("example:create"))])
def create_example(
    data: ExampleCreate,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """创建示例接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        example_service = ExampleService(db)
        example = example_service.create_example(tenant_id, data)
        
        return ResponseUtils.success(data={
            "id": example.id,
            "name": example.name,
            "code": example.code,
            "create_time": example.create_time.isoformat() if hasattr(example.create_time, 'isoformat') else example.create_time
        }, message="创建示例成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.put("/{example_id}", response_model=AuthResponse, summary="更新示例", dependencies=[Depends(permission_dependency("example:update"))])
def update_example(
    example_id: int,
    data: ExampleUpdate,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """更新示例接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        example_service = ExampleService(db)
        example = example_service.update_example(example_id, tenant_id, data)
        
        return ResponseUtils.success(data={
            "id": example.id,
            "name": example.name,
            "update_time": example.update_time.isoformat() if hasattr(example.update_time, 'isoformat') else example.update_time
        }, message="更新示例成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.delete("/{example_id}", response_model=AuthResponse, summary="删除示例", dependencies=[Depends(permission_dependency("example:delete"))])
def delete_example(
    example_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """删除示例接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        example_service = ExampleService(db)
        example_service.delete_example(example_id, tenant_id)
        
        return ResponseUtils.success(message="删除示例成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)
```

#### 步骤6：注册路由

文件：`App/Api/V1/__init__.py`

```python
"""API V1 Version"""

from fastapi import APIRouter
from App.Api.V1 import (
    Auth, Users, Roles, Permissions, Departments, Menus, Metrics,
    SystemDicts, SystemConfigs, OperationLogs, AuditLogs, UserGroups,
    DataPermissionRules, UserSessions, UserProfiles,
    Examples  # 添加新模块
)


# 创建V1版本的API路由
api_v1_router = APIRouter(prefix="/v1")

# ... 其他路由注册 ...

# 注册示例路由
api_v1_router.include_router(Examples.router)
```

---

## 测试指南

### 运行测试

```bash
# 运行所有测试
pytest

# 运行指定文件
pytest Tests/test_enterprise_monitoring.py

# 运行指定测试函数
pytest Tests/test_round18_demo.py::test_alert_escalation_manager

# 显示详细输出
pytest -v

# 生成覆盖率报告
pytest --cov=App --cov-report=html
```

### 测试文件位置

- `Tests/test_enterprise_monitoring.py` - 企业监控测试
- `Tests/test_round18_demo.py` - 第18轮优化演示
- `Tests/test_documentation.md` - 测试文档

---

## 部署指南

### 生产环境部署

#### 1. 使用Gunicorn + Uvicorn

```bash
# 安装Gunicorn
pip install gunicorn

# 启动服务
gunicorn App.Main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --access-logfile ./Logs/access.log \
    --error-logfile ./Logs/error.log
```

#### 2. 使用Docker

创建 `Dockerfile`：

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p Logs Uploads

EXPOSE 8000

CMD ["uvicorn", "App.Main:app", "--host", "0.0.0.0", "--port", "8000"]
```

构建并运行：

```bash
docker build -t rbac-system .
docker run -d -p 8000:8000 --name rbac-app rbac-system
```

#### 3. 使用Docker Compose

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql+pymysql://user:password@mysql:3306/rbac?charset=utf8mb4
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - mysql
      - redis
    volumes:
      - ./Logs:/app/Logs
      - ./Uploads:/app/Uploads

  mysql:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=rootpassword
      - MYSQL_DATABASE=rbac
    volumes:
      - mysql-data:/var/lib/mysql

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data

volumes:
  mysql-data:
  redis-data:
```

---

## 最佳实践

### 1. 代码规范

#### 命名规范

- **模块/文件**：小写+下划线 (snake_case)
- **类名**：大驼峰 (PascalCase)
- **函数/方法**：小写+下划线 (snake_case)
- **常量**：大写+下划线 (UPPER_CASE)
- **私有成员**：单下划线前缀 (_private)

#### 导入顺序

```python
# 1. 标准库
import os
import sys
from typing import List, Optional

# 2. 第三方库
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# 3. 本地模块
from App.Config.Settings import settings
from App.Models.User import UserModel
from App.Utils.Logger import logger
```

### 2. 数据库操作

#### 使用Repository模式

```python
# ✅ 推荐：使用Repository
user = user_repo.get_by_id(user_id)

# ❌ 避免：直接在Service中写SQL
user = db.query(UserModel).filter(UserModel.id == user_id).first()
```

#### 事务管理

```python
from sqlalchemy import text

# 使用事务
try:
    # 执行多个操作
    user_repo.create(user)
    role_repo.create(role)
    db.commit()
except Exception as e:
    db.rollback()
    raise e
```

### 3. 错误处理

#### 使用自定义异常

```python
from App.Core.Exceptions import CustomException

# 抛出异常
raise CustomException(
    status_code=400,
    detail="用户名已存在",
    error_code=40001
)

# 或使用HTTPException
from fastapi import HTTPException

raise HTTPException(status_code=404, detail="资源不存在")
```

### 4. 日志使用

```python
from App.Utils.Logger import logger

# 不同级别的日志
logger.debug("调试信息")
logger.info("普通信息")
logger.warning("警告信息")
logger.error("错误信息")
logger.critical("严重错误")

# 带参数的日志
logger.info(f"用户 {user_id} 登录成功，IP: {ip}")
```

### 5. 缓存使用

```python
from App.Utils.Cache import cache

# 设置缓存
cache.set("user:1", user_data, expire=3600)

# 获取缓存
user_data = cache.get("user:1")

# 删除缓存
cache.delete("user:1")
```

---

## 常见问题

### Q1: 如何添加新的权限？

A:
1. 在数据库中插入权限记录
2. 或通过API创建权限：`POST /api/v1/permissions`
3. 为角色分配该权限：`POST /api/v1/roles/{role_id}/permissions`

### Q2: JWT Token过期了怎么办？

A: 使用 `refresh_token` 调用 `POST /api/v1/auth/refresh` 获取新的 `access_token`。

### Q3: 如何初始化数据？

A: 可以编写初始化脚本，使用Service层创建初始数据（管理员用户、角色、权限等）。

### Q4: 如何调试SQL查询？

A: 在 `.env` 中设置 `APP_DEBUG=True`，SQLAlchemy会打印所有SQL语句。

### Q5: 多租户如何实现？

A: 所有数据表都有 `tenant_id` 字段，查询时通过 `tenant_id` 进行数据隔离。

### Q6: 如何添加新的中间件？

A: 在 `App/Core/Middleware.py` 中添加，然后在 `App/Main.py` 中注册。

---

## 附录

### A. 参考链接

- [FastAPI官方文档](https://fastapi.tiangolo.com/)
- [SQLAlchemy文档](https://docs.sqlalchemy.org/)
- [Pydantic文档](https://docs.pydantic.dev/)

### B. 联系方式

如有问题，请联系开发团队。

---

**文档版本**: v1.0.0
**最后更新**: 2026-04-11
