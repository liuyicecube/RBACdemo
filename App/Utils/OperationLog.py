"""Operation Log Utils - 操作日志工具类"""

import json
from fastapi import Request
from App.Models.OperationLog import OperationLogModel
from App.Config.Database import SessionLocal


class OperationLogUtils:
    """操作日志工具类"""

    @staticmethod
    def extract_module_from_path(path):
        """从URL路径提取模块名"""
        path_parts = path.strip("/").split("/")
        count = len(path_parts)
        if count >= 3:
            return path_parts[2]
        elif count >= 2:
            return path_parts[1]
        return "system"

    @staticmethod
    def extract_operation_from_method(method):
        """从HTTP方法提取操作类型"""
        method_map = {
            "GET": "查询",
            "POST": "创建",
            "PUT": "更新",
            "PATCH": "更新",
            "DELETE": "删除"
        }
        return method_map.get(method, "操作")

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
            operation = OperationLogUtils.extract_operation_from_method(request.method)

            request_params = {}
            if request.query_params:
                request_params.update(dict(request.query_params))

            request_body = None
            if hasattr(request, "body") and request.method in ["POST", "PUT", "PATCH"]:
                try:
                    body_bytes = await request.body()
                    if body_bytes:
                        request_body = body_bytes.decode("utf-8")
                        try:
                            request_params.update(json.loads(request_body))
                        except:
                            request_params["raw_body"] = request_body
                except:
                    pass

            params_str = json.dumps(request_params, ensure_ascii=False) if request_params else None

            status = 1 if response_status_code < 400 else 0

            db = SessionLocal()
            try:
                log = OperationLogModel(
                    tenant_id=1,
                    user_id=int(user_id) if user_id and user_id != "-" else None,
                    username=username,
                    module=module,
                    operation=operation,
                    request_method=request.method,
                    request_url=str(request.url),
                    ip_address=request.client.host if request.client else None,
                    user_agent=request.headers.get("user-agent"),
                    request_params=OperationLogUtils._mask_sensitive_data(params_str),
                    response_result=OperationLogUtils._mask_sensitive_data(response_body),
                    status=status,
                    error_message=error_message,
                    execution_time=int(execution_time_ms)
                )
                db.add(log)
                db.commit()
            except Exception as e:
                db.rollback()
                print(f"[OperationLog] Failed to save log: {e}")
            finally:
                db.close()

        except Exception as e:
            print(f"[OperationLog] Error in log_operation: {e}")

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
