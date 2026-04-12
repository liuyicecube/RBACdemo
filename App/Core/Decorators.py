
"""Decorators - 装饰器"""

from functools import wraps
from fastapi import Request
from App.Config.Database import SessionLocal
from App.Models.OperationLog import OperationLogModel
import json
import time


def log_operation(module, operation, description=None):
    """
    操作日志装饰器

    Args:
        module: 模块名称
        operation: 操作类型
        description: 操作描述
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = None
            db = None
            
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                if hasattr(arg, 'query') and hasattr(arg, 'add'):
                    db = arg
            
            if not db:
                for kwarg in kwargs.values():
                    if hasattr(kwarg, 'query') and hasattr(kwarg, 'add'):
                        db = kwarg
                        break
            
            start_time = time.time()
            error_message = None
            status = 1
            
            try:
                result = await func(*args, **kwargs) if hasattr(func, '__await__') else func(*args, **kwargs)
                return result
            except Exception as e:
                status = 0
                error_message = str(e)
                import traceback
                error_message += "\n" + traceback.format_exc()
                raise
            finally:
                execution_time = int((time.time() - start_time) * 1000)
                
                if request:
                    try:
                        user_id = getattr(request.state, "user_id", None)
                        username = getattr(request.state, "username", None)
                        
                        if user_id and user_id != "-":
                            log_db = SessionLocal()
                            try:
                                request_params = {}
                                if request.query_params:
                                    request_params.update(dict(request.query_params))
                                
                                log = OperationLogModel(
                                    tenant_id=1,
                                    user_id=int(user_id) if user_id and user_id != "-" else None,
                                    username=username,
                                    module=module,
                                    operation=operation,
                                    description=description,
                                    request_method=request.method,
                                    request_url=str(request.url),
                                    ip_address=request.client.host if request.client else None,
                                    user_agent=request.headers.get("user-agent"),
                                    request_params=json.dumps(request_params, ensure_ascii=False) if request_params else None,
                                    status=status,
                                    error_message=error_message,
                                    execution_time=execution_time
                                )
                                log_db.add(log)
                                log_db.commit()
                            except Exception as log_err:
                                log_db.rollback()
                                print(f"[LogDecorator] Failed to save log: {log_err}")
                            finally:
                                log_db.close()
                    except Exception as e:
                        print(f"[LogDecorator] Error: {e}")
        
        return wrapper
    return decorator

