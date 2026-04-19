# 企业级RBAC系统

## 项目概述

企业级RBAC系统是一个功能完善的权限管理系统，包含后端API服务和前端管理界面。系统提供用户管理、角色管理、权限管理、部门管理、菜单管理、字典管理、日志审计等核心功能。

---

## 技术栈

### 后端技术栈

- **Web框架**: FastAPI 0.104.0
- **ASGI服务器**: Uvicorn 0.24.0
- **ORM**: SQLAlchemy 2.0.0
- **数据库**: MySQL 8.0+ (使用PyMySQL驱动)
- **缓存**: Redis 5.0.0
- **数据验证**: Pydantic 2.5.0
- **安全认证**: JWT (python-jose) + BCrypt
- **日志**: Loguru 0.7.2
- **迁移工具**: Alembic 1.12.0
- **包管理**: Poetry

### 前端技术栈

- **前端框架**: Vue 3.4.21
- **构建工具**: Vite 5.2.6
- **UI组件库**: Element Plus 2.6.1
- **状态管理**: Pinia 2.1.7
- **路由**: Vue Router 4.3.0
- **HTTP客户端**: Axios 1.6.8
- **样式预处理**: Sass 1.72.0
- **类型检查**: TypeScript 5.4.3
- **测试框架**: Vitest 1.4.0
- **代码规范**: ESLint + Prettier

---

## 项目结构

```
pythonwebapi/
├── enterprise-rbac-system/          # 后端项目
│   ├── App/                         # 应用代码
│   │   ├── Api/                     # API路由
│   │   ├── Config/                  # 配置文件
│   │   ├── Core/                    # 核心组件
│   │   ├── Dependencies/            # 依赖注入
│   │   ├── Models/                  # 数据模型
│   │   ├── Repositories/            # 数据访问层
│   │   ├── Schemas/                 # 数据传输对象
│   │   ├── Services/                # 业务逻辑层
│   │   ├── Utils/                   # 工具函数
│   │   └── Main.py                  # 应用入口
│   ├── Logs/                        # 日志目录
│   ├── Migrations/                  # 迁移脚本
│   ├── Requirements/                # 依赖文件
│   ├── Scripts/                     # 初始化脚本
│   ├── Tests/                       # 测试文件
│   ├── .env                         # 环境变量配置
│   ├── .env.example                 # 环境变量示例
│   ├── PyProject.toml               # Poetry配置
│   └── README.md                    # 后端详细文档
│
└── enterprise-rbac-system-UIAPP/    # 前端项目
    ├── dist/                        # 构建输出目录
    ├── src/                         # 源代码
    │   ├── assets/                  # 静态资源
    │   ├── components/              # 组件
    │   ├── constants/               # 常量定义
    │   ├── directives/              # 自定义指令
    │   ├── router/                  # 路由配置
    │   ├── services/                # API服务
    │   ├── store/                   # 状态管理
    │   ├── styles/                  # 样式文件
    │   ├── types/                   # TypeScript类型定义
    │   ├── utils/                   # 工具函数
    │   ├── views/                   # 页面组件
    │   ├── App.vue                  # 根组件
    │   └── main.ts                  # 应用入口
    ├── .env.development             # 开发环境变量
    ├── .env.production              # 生产环境变量
    ├── index.html                   # HTML入口
    ├── package.json                 # npm配置
    ├── tsconfig.json                # TypeScript配置
    ├── vite.config.ts               # Vite配置
    └── README.md                    # 前端详细文档
```

---

## 代码统计

### 后端代码统计
- **文件总数**: 135 个
- **代码总行数**: 15,399 行

### 前端代码统计
- **文件总数**: 68 个
- **代码总行数**: 21,556 行

### 总体代码统计
- **总文件数**: 203 个
- **总代码行数**: 36,955 行

---

## 系统要求

### 后端系统要求

- Python 3.10 或更高版本
- MySQL 8.0 或更高版本
- Redis 5.0 或更高版本
- 至少 2GB RAM
- 至少 10GB 磁盘空间

### 前端系统要求

- Node.js 18.0 或更高版本
- npm 9.0 或更高版本（或yarn/pnpm）
- 现代浏览器（Chrome 90+、Firefox 88+、Edge 90+、Safari 14+）
- 至少 2GB RAM
- 至少 5GB 磁盘空间

---

## 快速开始

### 后端启动

```bash
cd enterprise-rbac-system
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
pip install -r Requirements/Dev.txt
cp .env.example .env
# 编辑 .env 文件配置数据库和Redis
python App/Main.py
```

后端服务将在 `http://localhost:8000` 启动，API文档访问 `http://localhost:8000/docs`。

### 前端启动

```bash
cd enterprise-rbac-system-UIAPP
npm install
npm run dev
```

前端开发服务器将在 `http://localhost:5173` 启动。

---

## 功能特性

### 核心功能

- **用户管理**: 用户增删改查、状态管理、密码重置
- **角色管理**: 角色定义、角色权限分配、用户角色关联
- **权限管理**: 权限定义、权限分组
- **部门管理**: 部门树形结构、部门用户管理
- **菜单管理**: 菜单树形结构、菜单权限配置
- **字典管理**: 系统字典、字典项管理
- **用户组管理**: 用户组定义、组角色分配
- **数据权限**: 数据权限规则配置
- **日志审计**: 操作日志、审计日志
- **会话管理**: 在线用户查看、会话强制下线
- **系统设置**: 系统参数配置

### 安全特性

- JWT令牌认证
- 密码BCrypt加密
- 角色权限控制
- 数据权限控制
- 操作日志记录
- 安全头配置

---

## 详细文档

- [后端详细文档](./enterprise-rbac-system/README.md) - 包含后端部署、配置、开发指南
- [前端详细文档](./enterprise-rbac-system-UIAPP/README.md) - 包含前端部署、配置、开发指南

---

## 许可证

本项目采用MIT许可证。

---

**最后更新**: 2026-04-19
