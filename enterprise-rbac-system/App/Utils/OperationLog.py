"""Operation Log Utils - 操作日志工具类"""

import json
from fastapi import Request
from App.Models.OperationLog import OperationLogModel
from App.Config.Database import SessionLocal


class OperationLogUtils:
    """操作日志工具类"""

    @staticmethod
    def extract_module_from_path(path):
        """从URL路径提取模块名称"""
        path = path.lower()
        
        # 特殊路径处理
        if "/auth/login" in path:
            return "用户管理"
        elif "/auth/logout" in path:
            return "用户管理"
        elif "/auth/register" in path:
            return "用户管理"
        elif "/users" in path:
            return "用户管理"
        elif "/roles" in path:
            return "角色管理"
        elif "/departments" in path:
            return "部门管理"
        elif "/permissions" in path:
            return "权限管理"
        elif "/menus" in path:
            return "菜单管理"
        elif "/operation-logs" in path:
            return "日志管理"
        
        # 默认处理
        path_parts = path.strip("/").split("/")
        count = len(path_parts)
        if count >= 3:
            return path_parts[2]
        elif count >= 2:
            return path_parts[1]
        return "系统"

    @staticmethod
    def extract_operation_from_path_and_method(path, method):
        """从URL路径和HTTP方法提取操作类型"""
        path = path.lower()
        
        # 特殊路径处理
        if "/auth/login" in path:
            return "登录"
        elif "/auth/logout" in path:
            return "退出登录"
        elif "/auth/register" in path:
            return "注册"
        elif "/auth/change-password" in path or "/auth/reset-password" in path:
            return "修改密码"
        elif "/auth/refresh" in path:
            return "刷新Token"
        
        # 默认按HTTP方法处理
        method_map = {
            "GET": "查询",
            "POST": "创建",
            "PUT": "更新",
            "PATCH": "更新",
            "DELETE": "删除"
        }
        return method_map.get(method, "操作")

    @staticmethod
    def generate_description(path, method, module, operation):
        """生成操作描述"""
        path = path.lower()
        
        if "/auth/login" in path:
            return "用户登录系统"
        elif "/auth/logout" in path:
            return "用户退出登录"
        elif "/auth/register" in path:
            return "用户注册账户"
        elif "/auth/change-password" in path:
            return "修改用户密码"
        elif "/auth/reset-password" in path:
            return "重置用户密码"
        elif "/users" in path and method == "GET":
            return "查询用户列表"
        elif "/users" in path and method == "POST":
            return "创建新用户"
        elif "/users" in path and method == "PUT":
            return "更新用户信息"
        elif "/users" in path and method == "DELETE":
            return "删除用户"
        elif "/roles" in path and method == "GET":
            return "查询角色列表"
        elif "/roles" in path and method == "POST":
            return "创建新角色"
        elif "/roles" in path and method == "PUT":
            return "更新角色信息"
        elif "/roles" in path and method == "DELETE":
            return "删除角色"
        elif "/operation-logs" in path and method == "GET":
            return "查询操作日志"
        
        return f"{operation}{module}数据"

    @staticmethod
    async def log_operation(
        request,
        response_status_code,
        execution_time_ms,
        response_body=None,
        error_message=None
    ):
        """
        记录操作日志到数据库

        Args:
            request: FastAPI Request对象
            response_status_code: HTTP响应状态码
            execution_time_ms: 执行时长(毫秒)
            response_body: 响应体内容
            error_message: 错误信息
        """
        try:
            user_id = getattr(request.state, "user_id", None)
            username = getattr(request.state, "username", None)

            if user_id == "-":
                user_id = None

            module = OperationLogUtils.extract_module_from_path(request.url.path)
            operation = OperationLogUtils.extract_operation_from_path_and_method(request.url.path, request.method)
            description = OperationLogUtils.generate_description(request.url.path, request.method, module, operation)

            request_params = {}
            if hasattr(request, "query_params") and request.query_params:
                try:
                    request_params.update(dict(request.query_params))
                except:
                    pass

            # 注意：不要在 finally 块中读取 request.body，因为请求流可能已经被消费
            # 而且多次读取会有问题

            params_str = None
            try:
                params_str = json.dumps(request_params, ensure_ascii=False) if request_params else None
            except:
                pass

            status = 1 if response_status_code < 400 else 0

            db = SessionLocal()
            try:
                log = OperationLogModel(
                    tenant_id=1,
                    user_id=int(user_id) if (user_id and user_id != "-" and user_id is not None) else None,
                    username=username,
                    module=module,
                    operation=operation,
                    description=description,
                    request_method=request.method,
                    request_url=str(request.url),
                    ip_address=request.client.host if (hasattr(request, "client") and request.client) else None,
                    user_agent=request.headers.get("user-agent") if hasattr(request, "headers") else None,
                    request_params=OperationLogUtils._mask_sensitive_data(params_str),
                    response_result=OperationLogUtils._mask_sensitive_data(response_body),
                    status=status,
                    error_message=error_message,
                    execution_time=int(execution_time_ms) if execution_time_ms is not None else 0
                )
                db.add(log)
                db.commit()
            except Exception as e:
                db.rollback()
            finally:
                db.close()

        except Exception as e:
            pass

    @staticmethod
    def _mask_sensitive_data(data):
        """掩码敏感数据"""
        if not data:
            return data

        sensitive_keys = [
            "password", "token", "secret", "credit_card", "ssn",
            "phone", "email", "authorization", "bearer"
        ]

        try:
            data_dict = json.loads(data)
            if isinstance(data_dict, dict):
                masked_dict = data_dict.copy()
                for key in masked_dict:
                    flag = False
                    for sensitive in sensitive_keys:
                        if sensitive in key.lower():
                            flag = True
                            break
                    if flag:
                        masked_dict[key] = "***"
                return json.dumps(masked_dict, ensure_ascii=False)
        except:
            pass

        return data
