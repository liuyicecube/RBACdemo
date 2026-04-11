"""Authentication Dependencies"""

from fastapi import Depends, Request
from sqlalchemy.orm import Session
from App.Models.User import UserModel
from App.Core.Exceptions import AuthenticationException
from App.Dependencies.Database import get_db


def get_current_user(request: Request, db: Session = Depends(get_db)) -> UserModel:
    """获取当前用户"""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise AuthenticationException(detail="缺少Authorization头")
    
    if not auth_header.startswith("Bearer "):
        raise AuthenticationException(detail="无效的Authorization头格式")
    
    token = auth_header.replace("Bearer ", "")
    
    from App.Core.Security import SecurityCore
    payload = SecurityCore.verify_token(token)
    if not payload:
        raise AuthenticationException(detail="无效的token")
    
    if payload.get("token_type") != "access":
        raise AuthenticationException(detail="无效的token类型")
    
    user_id = payload.get("sub")
    if not user_id:
        raise AuthenticationException(detail="未获取到用户信息")
    
    user = db.query(UserModel).filter(UserModel.id == int(user_id), UserModel.status == 1).first()
    
    if not user:
        raise AuthenticationException(detail="用户不存在或已禁用")
    
    return user


def get_current_user_and_tenant_id(request: Request, db: Session = Depends(get_db)):
    """获取当前用户和租户ID"""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise AuthenticationException(detail="缺少Authorization头")
    
    if not auth_header.startswith("Bearer "):
        raise AuthenticationException(detail="无效的Authorization头格式")
    
    token = auth_header.replace("Bearer ", "")
    
    from App.Core.Security import SecurityCore
    payload = SecurityCore.verify_token(token)
    if not payload:
        raise AuthenticationException(detail="无效的token")
    
    if payload.get("token_type") != "access":
        raise AuthenticationException(detail="无效的token类型")
    
    user_id = payload.get("sub")
    tenant_id = payload.get("tenant_id")
    if not user_id:
        raise AuthenticationException(detail="未获取到用户信息")
    
    user = db.query(UserModel).filter(UserModel.id == int(user_id), UserModel.status == 1).first()
    
    if not user:
        raise AuthenticationException(detail="用户不存在或已禁用")
    
    return user, tenant_id or user.tenant_id


def get_current_user_id(request: Request) -> int:
    """获取当前用户ID"""
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise AuthenticationException(detail="未获取到用户信息")
    
    try:
        return int(user_id)
    except (ValueError, TypeError):
        raise AuthenticationException(detail="用户ID格式无效")
