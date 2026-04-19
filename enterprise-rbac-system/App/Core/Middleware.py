"""Middleware Core"""

from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from App.Config.Settings import settings
from App.Core.Security import SecurityCore
from App.Utils.Response import ResponseUtils
from App.Services.UserSessionService import UserSessionService


class MiddlewareCore:
    """中间件核心功能"""

    @staticmethod
    def add_cors_middleware(app):
        """添加CORS中间件"""
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins_list,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    @staticmethod
    def add_security_headers_middleware(app):
        """添加安全头中间件"""
        @app.middleware("http")
        async def security_headers_middleware(request: Request, call_next):
            response = await call_next(request)
            # 添加安全头
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "img-src 'self' data: https://fastapi.tiangolo.com; "
                "font-src 'self' data:; "
                "connect-src 'self' https://cdn.jsdelivr.net; "
                "frame-ancestors 'none'; "
                "base-uri 'self'; "
                "form-action 'self';"
            )
            return response

    @staticmethod
    async def authentication_middleware(request: Request, call_next):
        """认证中间件"""

        # 处理OPTIONS请求（CORS preflight）
        if request.method == "OPTIONS":
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

        # 检查前缀匹配
        for prefix in prefix_match_paths:
            if request.url.path.startswith(prefix):
                skip_auth = True
                break

        if skip_auth:
            return await call_next(request)

        # 获取Authorization头
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return ResponseUtils.unauthorized(message="缺少Authorization头")

        # 检查Bearer前缀
        if not auth_header.startswith("Bearer "):
            return ResponseUtils.unauthorized(message="无效的Authorization头格式")

        # 提取token
        token = auth_header.replace("Bearer ", "")

        # 验证token
        payload = SecurityCore.verify_token(token)
        if not payload:
            # 在调试模式下，跳过token验证
            if settings.app_debug:
                # 模拟一个payload
                payload = {"sub": "1", "username": "test_user", "token_type": "access"}
            else:
                return ResponseUtils.unauthorized(message="无效的token")

        # 检查token类型
        if payload.get("token_type") != "access":
            return ResponseUtils.unauthorized(message="无效的token类型")

        # 检查会话状态
        session_id = payload.get("session_id")
        tenant_id = payload.get("tenant_id")
        if session_id:
            try:
                from App.Core.Database import SessionLocal
                db = SessionLocal()
                try:
                    from App.Repositories.UserSessionRepository import UserSessionRepository
                    session_repo = UserSessionRepository(db)
                    session = session_repo.get_by_session_id(session_id, tenant_id=tenant_id)
                    
                    if not session or session.status != 1:
                        return ResponseUtils.unauthorized(message="会话已过期，请重新登录")
                finally:
                    db.close()
            except Exception as e:
                import traceback

        # 将用户信息存储到请求状态
        request.state.user_id = payload.get("sub")
        request.state.username = payload.get("username")

        response = await call_next(request)
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
            "/favicon.ico", "/vite.svg"
        ]
        
        skip_log_prefixes = [
            "/static", "/assets"
        ]
        
        should_log_db = True
        # 检查精确匹配
        if request.url.path in skip_log_paths:
            should_log_db = False
        else:
            # 检查前缀匹配
            for prefix in skip_log_prefixes:
                if request.url.path.startswith(prefix):
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
        response_body = None
        
        try:
            response = await call_next(request)
            response_status_code = response.status_code
            
            # 读取响应体
            if 'application/json' in response.headers.get('content-type', ''):
                response_body_bytes = b''
                async for chunk in response.body_iterator:
                    response_body_bytes += chunk
                
                # 重新构建响应
                from fastapi.responses import Response
                response = Response(
                    content=response_body_bytes,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.media_type
                )
                
                try:
                    response_body = response_body_bytes.decode('utf-8')
                except:
                    response_body = None
            
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
                        response_body=response_body,
                        error_message=error_message
                    )
                except Exception as log_err:
                    pass

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
