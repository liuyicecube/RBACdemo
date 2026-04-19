# 企业级RBAC系统 - 前端部署文档

## 项目概述

企业级RBAC系统前端是一个基于Vue 3构建的权限管理系统，提供用户管理、角色管理、权限管理、部门管理等功能的可视化界面。

### 技术栈

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

### 系统要求

- Node.js 18.0 或更高版本
- npm 9.0 或更高版本（或yarn/pnpm）
- 现代浏览器（Chrome 90+、Firefox 88+、Edge 90+、Safari 14+）
- 至少 2GB RAM
- 至少 5GB 磁盘空间

---

## 目录结构

```
enterprise-rbac-system-UIAPP/
├── dist/                  # 构建输出目录
├── src/
│   ├── assets/           # 静态资源
│   │   └── styles/       # 全局样式
│   ├── components/       # 组件
│   │   ├── __tests__/    # 组件测试
│   │   └── layout/       # 布局组件
│   ├── constants/        # 常量定义
│   ├── directives/       # 自定义指令
│   ├── router/           # 路由配置
│   ├── services/         # API服务
│   ├── store/            # 状态管理（Pinia）
│   │   └── modules/      # 状态模块
│   ├── styles/           # 样式文件
│   ├── types/            # TypeScript类型定义
│   ├── utils/            # 工具函数
│   │   └── __tests__/    # 工具函数测试
│   ├── views/            # 页面组件
│   │   ├── auth/         # 认证相关页面
│   │   ├── dashboard/    # 仪表板
│   │   ├── dataPermissions/  # 数据权限
│   │   ├── departments/  # 部门管理
│   │   ├── dictionaries/ # 字典管理
│   │   ├── error/        # 错误页面
│   │   ├── logs/         # 日志管理
│   │   ├── menus/        # 菜单管理
│   │   ├── permissions/  # 权限管理
│   │   ├── roles/        # 角色管理
│   │   ├── sessions/     # 会话管理
│   │   ├── settings/     # 系统设置
│   │   └── users/        # 用户管理
│   ├── App.vue           # 根组件
│   └── main.ts           # 应用入口
├── .env.development      # 开发环境变量
├── .env.production       # 生产环境变量
├── .gitignore
├── index.html            # HTML入口
├── package.json
├── tsconfig.json
├── tsconfig.node.json
├── vite.config.ts        # Vite配置
└── vitest.config.ts      # Vitest配置
```

---

## 部署步骤

### 1. 环境准备

#### 1.1 安装Node.js

从 [Node.js官网](https://nodejs.org/) 下载并安装LTS版本（推荐18.x或20.x）。

验证安装：

```bash
node --version
npm --version
```

#### 1.2 安装包管理器（可选）

推荐使用pnpm或yarn：

```bash
# 使用pnpm
npm install -g pnpm

# 或使用yarn
npm install -g yarn
```

### 2. 项目安装

#### 2.1 进入项目目录

```bash
cd enterprise-rbac-system-UIAPP
```

#### 2.2 安装依赖

使用npm：

```bash
npm install
```

使用pnpm：

```bash
pnpm install
```

使用yarn：

```bash
yarn install
```

### 3. 配置环境变量

#### 3.1 开发环境配置

复制或编辑 `.env.development`：

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

配置说明：
- `VITE_API_BASE_URL`: 后端API地址

#### 3.2 生产环境配置

复制或编辑 `.env.production`：

```env
VITE_API_BASE_URL=/api/v1
```

**注意**: 生产环境建议使用相对路径或Nginx反向代理，避免跨域问题。

### 4. 开发环境运行

启动开发服务器：

```bash
npm run dev
```

或使用pnpm/yarn：

```bash
pnpm dev
# 或
yarn dev
```

开发服务器将在 `http://localhost:5173` 启动，浏览器会自动打开。

#### 开发服务器配置

在 `vite.config.ts` 中配置了开发代理：

```typescript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true
  }
}
```

这样前端请求 `/api` 会被代理到后端的 `http://localhost:8000`。

### 5. 生产环境构建

#### 5.1 构建项目

```bash
npm run build
```

或使用pnpm/yarn：

```bash
pnpm build
# 或
yarn build
```

构建完成后，文件会输出到 `dist/` 目录。

#### 5.2 预览构建结果

```bash
npm run preview
```

这会在本地启动一个服务器预览构建后的应用。

### 6. 生产环境部署

#### 6.1 使用Nginx部署

##### 步骤1：上传构建文件

将 `dist/` 目录下的所有文件上传到服务器的Web目录，例如 `/var/www/rbac-ui/`。

##### 步骤2：配置Nginx

创建Nginx配置文件 `/etc/nginx/sites-available/rbac-ui`：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /var/www/rbac-ui;
    index index.html;

    # Gzip压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json application/javascript;

    # 安全头
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    add_header Referrer-Policy "strict-origin-when-cross-origin";

    # 前端静态资源
    location / {
        try_files $uri $uri/ /index.html;
        
        # 缓存策略
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
        
        location ~* \.html$ {
            expires -1;
            add_header Cache-Control "no-cache, no-store, must-revalidate";
        }
    }

    # API反向代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # 禁止访问隐藏文件
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
}
```

##### 步骤3：启用站点

```bash
sudo ln -s /etc/nginx/sites-available/rbac-ui /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 6.2 使用Caddy部署

创建 `Caddyfile`：

```
your-domain.com {
    root * /var/www/rbac-ui
    file_server

    # SPA路由支持
    try_files {path} /index.html

    # API代理
    reverse_proxy /api/* 127.0.0.1:8000

    # 缓存配置
    @static {
        path *.js *.css *.png *.jpg *.jpeg *.gif *.ico *.svg *.woff *.woff2 *.ttf *.eot
    }
    header @static Cache-Control "public, max-age=31536000, immutable"

    # 安全头
    header {
        X-Content-Type-Options nosniff
        X-Frame-Options DENY
        X-XSS-Protection "1; mode=block"
        Referrer-Policy strict-origin-when-cross-origin
    }
}
```

启动Caddy：

```bash
caddy run
```

#### 6.3 使用Docker部署

创建 `Dockerfile`：

```dockerfile
# 构建阶段
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# 生产阶段
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

创建 `nginx.conf`：

```nginx
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    server {
        listen 80;
        server_name localhost;
        root /usr/share/nginx/html;
        index index.html;

        gzip on;
        gzip_vary on;
        gzip_min_length 1024;
        gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json application/javascript;

        location / {
            try_files $uri $uri/ /index.html;
        }

        location /api/ {
            proxy_pass http://backend:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}
```

构建和运行：

```bash
docker build -t rbac-ui .
docker run -d -p 80:80 --name rbac-ui --network rbac-network rbac-ui
```

#### 6.4 使用PM2 + serve部署

安装serve：

```bash
npm install -g serve
```

创建 `ecosystem.config.js`：

```javascript
module.exports = {
  apps: [{
    name: 'rbac-ui',
    script: 'npx',
    args: 'serve -s dist -l 3000',
    cwd: '/path/to/enterprise-rbac-system-UIAPP',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G'
  }]
};
```

启动应用：

```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

### 7. SSL证书配置（生产环境必须）

#### 使用Let's Encrypt + Certbot（Nginx）

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

Certbot会自动配置Nginx并设置证书自动续期。

#### 使用Caddy

Caddy会自动申请和续期SSL证书，无需额外配置。

---

## 验证部署

### 1. 访问应用

在浏览器中访问：
```
http://your-domain.com
```

应该显示登录页面。

### 2. 功能测试

1. 登录系统
2. 访问各个功能页面
3. 测试增删改查操作
4. 验证权限控制

### 3. 检查API连接

打开浏览器开发者工具（F12），查看Network标签，确认API请求正常。

---

## 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| VITE_API_BASE_URL | 后端API地址 | http://localhost:8000/api/v1 |

### Vite配置

配置文件：`vite.config.ts`

主要配置项：

- **别名**: `@` 指向 `src/` 目录
- **开发代理**: `/api` 代理到 `http://localhost:8000`
- **开发端口**: 5173
- **安全头**: XSS防护、点击劫持防护等

### TypeScript配置

配置文件：`tsconfig.json`

- **target**: ES2020
- **module**: ESNext
- **strict**: 严格模式
- **路径别名**: `@/*` 映射到 `src/*`

---

## 开发指南

### 代码规范

运行代码检查：

```bash
npm run lint
```

格式化代码：

```bash
npm run format
```

### 运行测试

运行所有测试：

```bash
npm run test
```

运行测试并生成覆盖率报告：

```bash
npm run test:coverage
```

使用UI界面运行测试：

```bash
npm run test:ui
```

### 常用命令

| 命令 | 说明 |
|------|------|
| npm run dev | 启动开发服务器 |
| npm run build | 构建生产版本 |
| npm run preview | 预览构建结果 |
| npm run lint | 运行ESLint检查 |
| npm run format | 格式化代码 |
| npm run test | 运行测试 |

---

## 性能优化

### 1. 构建优化

Vite已经内置了许多优化：
- Tree Shaking
- 代码分割
- 懒加载
- 压缩

### 2. 缓存策略

在Nginx配置中设置了缓存策略：
- 静态资源（js、css、图片等）缓存1年
- HTML文件不缓存

### 3. Gzip压缩

启用Gzip压缩可以大幅减小传输体积。

---

## 安全建议

1. **HTTPS**: 生产环境必须使用HTTPS
2. **CSP**: 配置内容安全策略
3. **安全头**: 保持vite.config.ts中的安全头配置
4. **依赖更新**: 定期更新npm依赖包
5. **权限最小化**: Web服务器用户权限最小化

---

## 监控与维护

### 日志查看

- 浏览器控制台：按F12查看
- Nginx访问日志：`/var/log/nginx/access.log`
- Nginx错误日志：`/var/log/nginx/error.log`

### 常见问题

1. **页面刷新404**
   - 确保Nginx配置了 `try_files $uri $uri/ /index.html;`

2. **API请求失败**
   - 检查后端服务是否正常运行
   - 验证API地址配置
   - 检查CORS配置

3. **静态资源加载失败**
   - 检查文件权限
   - 验证Nginx root路径配置

4. **跨域问题**
   - 确保后端CORS配置包含前端域名
   - 或使用Nginx反向代理

---

## 更新与升级

### 更新依赖

```bash
npm outdated
npm update
```

### 部署更新

1. 拉取最新代码
2. 安装依赖（如果有变化）
3. 构建项目
4. 备份当前版本
5. 替换dist目录
6. 重启Web服务器（如需要）

```bash
cd /path/to/enterprise-rbac-system-UIAPP
git pull
npm install
npm run build
# 备份旧版本
cp -r /var/www/rbac-ui /var/www/rbac-ui.backup
# 部署新版本
cp -r dist/* /var/www/rbac-ui/
```

---

## 前后端联调

### 开发环境

1. 启动后端服务（端口8000）
2. 启动前端开发服务器（端口5173）
3. 前端会通过代理访问后端API

### 生产环境

1. 前后端部署在同一域名下
2. 前端通过 `/api` 路径访问后端
3. Nginx负责路由分发

---

## 浏览器支持

| 浏览器 | 最低版本 |
|--------|----------|
| Chrome | 90+ |
| Firefox | 88+ |
| Edge | 90+ |
| Safari | 14+ |

---

## 技术支持

如有问题，请查看：
- [Vue 3文档](https://cn.vuejs.org/)
- [Vite文档](https://cn.vitejs.dev/)
- [Element Plus文档](https://element-plus.org/zh-CN/)
- 项目Issues页面

---

## 许可证

本项目采用MIT许可证。

---

**最后更新**: 2026-04-19
