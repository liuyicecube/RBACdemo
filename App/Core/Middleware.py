"""Middleware Core"""

from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from App.Config.Settings import settings
from App.Core.Security import SecurityCore
from App.Utils.Response import ResponseUtils


class MiddlewareCore:
    """中间件核心功能"""

    @staticmethod
    def add_cors_middleware(app):
        """添加CORS中间件"""
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @staticmethod
    async def authentication_middleware(request: Request, call_next):
        """认证中间件"""
        print(f"[AuthMiddleware] Processing request: method={request.method}, path={request.url.path}")

        # 处理OPTIONS请求（CORS preflight）
        if request.method == "OPTIONS":
            print("[AuthMiddleware] Skipping OPTIONS request")
            return await call_next(request)

        # 跳过认证的路径
        skip_auth = False

        # 精确匹配的路径
        exact_match_paths = [
            "/", "/health", "/api/v1/auth/login", "/api/v1/auth/register", "/api/v1/auth/refresh", "/api/v1/auth/me", "/api/v1/auth/profile", "/api/v1/auth/logout", "/docs", "/redoc", "/openapi.json", "/favicon.ico", "/vite.svg",
            "/v1/auth/login", "/v1/auth/register", "/v1/auth/refresh", "/v1/auth/me", "/v1/auth/profile", "/v1/auth/logout"
        ]

        # 前缀匹配的路径
        prefix_match_paths = [
            "/static", "/assets", "/@vite"
        ]

        # 检查精确匹配
        if request.url.path in exact_match_paths:
            skip_auth = True
            print(f"[AuthMiddleware] Skipping auth (exact match): {request.url.path}")

        # 检查前缀匹配
        for prefix in prefix_match_paths:
            if request.url.path.startswith(prefix):
                skip_auth = True
                print(f"[AuthMiddleware] Skipping auth (prefix match): {request.url.path} starts with {prefix}")
                break

        if skip_auth:
            return await call_next(request)

        # 获取Authorization头
        auth_header = request.headers.get("Authorization")
        print(f"[AuthMiddleware] Authorization header: {'present' if auth_header else 'missing'}")
        if not auth_header:
            print("[AuthMiddleware] Returning 401: missing Authorization header")
            return ResponseUtils.unauthorized(message="缺少Authorization头")

        # 检查Bearer前缀
        if not auth_header.startswith("Bearer "):
            print(f"[AuthMiddleware] Returning 401: invalid Authorization header format - does not start with Bearer")
            return ResponseUtils.unauthorized(message="无效的Authorization头格式")

        # 提取token
        token = auth_header.replace("Bearer ", "")
        print(f"[AuthMiddleware] Extracted token: {token[:20]}... (truncated)")

        # 验证token
        payload = SecurityCore.verify_token(token)
        print(f"[AuthMiddleware] verify_token result: {'valid' if payload else 'invalid/None'}")
        if not payload:
            # 在调试模式下，跳过token验证
            print(f"DEBUG: app_debug is {settings.app_debug}")
            if settings.app_debug:
                print("DEBUG: Skipping token verification")
                # 模拟一个payload
                payload = {"sub": "1", "username": "test_user", "token_type": "access"}
            else:
                print("[AuthMiddleware] Returning 401: invalid token")
                return ResponseUtils.unauthorized(message="无效的token")

        print(f"[AuthMiddleware] Token payload: {payload}")

        # 检查token类型
        if payload.get("token_type") != "access":
            print(f"[AuthMiddleware] Returning 401: invalid token type {payload.get('token_type')}")
            return ResponseUtils.unauthorized(message="无效的token类型")

        # 将用户信息存储到请求状态
        request.state.user_id = payload.get("sub")
        request.state.username = payload.get("username")
        print(f"[AuthMiddleware] Request state set: user_id={request.state.user_id}, username={request.state.username}")

        response = await call_next(request)
        print(f"[AuthMiddleware] Response status code: {response.status_code}")
        return response

    @staticmethod
    async def logging_middleware(request: Request, call_next):
        """日志中间件"""
        import time
        import uuid
        from App.Utils.Logger import logger, LoggerUtils

        # 生成请求ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # 获取用户ID
        user_id = getattr(request.state, "user_id", "-")

        # 记录请求开始时间
        start_time = time.time()

        # 跳过日志记录的路径
        skip_log_paths = [
            "/", "/health", "/docs", "/redoc", "/openapi.json",
            "/favicon.ico", "/vite.svg", "/static", "/assets"
        ]
        
        should_log_db = True
        for path in skip_log_paths:
            if request.url.path.startswith(path):
                should_log_db = False
                break

        # 确保所有必要字段存在
        extra = {
            "request_id": request_id,
            "user_id": user_id,
            "method": request.method,
            "url": str(request.url)
        }

        # 记录请求信息
        logger.info(
            f"Request received",
            **extra
        )

        # 处理请求
        error_message = None
        response_status_code = 200
        
        try:
            response = await call_next(request)
            response_status_code = response.status_code
        except Exception as e:
            error_message = str(e)
            import traceback
            error_message += "\n" + traceback.format_exc()
            response_status_code = 500
            raise
        finally:
            # 计算响应时间
            response_time = time.time() - start_time
            execution_time_ms = round(response_time * 1000, 2)

            # 记录性能日志
            LoggerUtils.log_performance(
                request_id=request_id,
                user_id=str(user_id),
                endpoint=request.url.path,
                method=request.method,
                status_code=response_status_code,
                response_time=response_time
            )

            if should_log_db:
                try:
                    from App.Utils.OperationLog import OperationLogUtils
                    await OperationLogUtils.log_operation(
                        request=request,
                        response_status_code=response_status_code,
                        execution_time_ms=execution_time_ms,
                        response_body=None,
                        error_message=error_message
                    )
                except Exception as log_err:
                    print(f"[Middleware] Failed to log to DB: {log_err}")

            # 确保所有必要字段存在
            extra = {
                "request_id": request_id,
                "user_id": user_id,
                "status_code": response_status_code,
                "response_time": execution_time_ms
            }

            # 记录响应信息
            logger.info(
                f"Response sent",
                **extra
            )

        return response
