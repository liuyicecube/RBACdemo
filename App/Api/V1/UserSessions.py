"""User Session Management API"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from App.Schemas.UserSession import KickUserRequest
from App.Schemas.Auth import AuthResponse
from App.Services.UserSessionService import UserSessionService
from App.Dependencies.Database import get_db
from App.Dependencies.Auth import get_current_user_and_tenant_id
from App.Dependencies.Permission import permission_dependency
from App.Utils.Logger import logger
from App.Utils.Response import ResponseUtils


router = APIRouter(
    prefix="/user-sessions",
    tags=["用户会话管理"]
)


@router.get(
    "",
    response_model=AuthResponse,
    summary="获取用户会话列表",
    dependencies=[Depends(permission_dependency("user_session:view"))]
)
def get_user_sessions(
    user_id: int = None,
    device_type: str = None,
    status: int = None,
    keyword: str = None,
    page: int = 1,
    page_size: int = 10,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取用户会话列表接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        session_service = UserSessionService(db)

        total, sessions = session_service.paginate_sessions(
            tenant_id=tenant_id,
            user_id=user_id,
            device_type=device_type,
            status=status,
            keyword=keyword,
            page=page,
            page_size=page_size
        )

        session_list = []
        for session in sessions:
            session_list.append({
                "id": session.id,
                "user_id": session.user_id,
                "session_id": session.session_id,
                "device_type": session.device_type,
                "device_info": session.device_info,
                "ip_address": session.ip_address,
                "login_time": session.login_time.isoformat() if hasattr(session.login_time, 'isoformat') else session.login_time,
                "last_active_time": session.last_active_time.isoformat() if hasattr(session.last_active_time, 'isoformat') else session.last_active_time,
                "expire_time": session.expire_time.isoformat() if hasattr(session.expire_time, 'isoformat') else session.expire_time,
                "status": session.status,
                "create_time": session.create_time.isoformat() if hasattr(session.create_time, 'isoformat') else session.create_time,
                "update_time": session.update_time.isoformat() if hasattr(session.update_time, 'isoformat') else session.update_time
            })

        return ResponseUtils.pagination(
            data=session_list,
            total=total,
            page=page,
            page_size=page_size,
            message="获取用户会话列表成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_user_sessions: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get(
    "/online",
    response_model=AuthResponse,
    summary="获取在线用户会话",
    dependencies=[Depends(permission_dependency("user_session:view"))]
)
def get_online_sessions(
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取在线用户会话接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        session_service = UserSessionService(db)
        sessions = session_service.get_all_active_sessions(tenant_id=tenant_id)

        session_list = []
        for session in sessions:
            session_list.append({
                "id": session.id,
                "user_id": session.user_id,
                "session_id": session.session_id,
                "device_type": session.device_type,
                "device_info": session.device_info,
                "ip_address": session.ip_address,
                "login_time": session.login_time.isoformat() if hasattr(session.login_time, 'isoformat') else session.login_time,
                "last_active_time": session.last_active_time.isoformat() if hasattr(session.last_active_time, 'isoformat') else session.last_active_time
            })

        return ResponseUtils.success(
            data={
                "total": len(session_list),
                "sessions": session_list
            },
            message="获取在线用户会话成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get(
    "/user/{user_id}",
    response_model=AuthResponse,
    summary="获取指定用户的会话",
    dependencies=[Depends(permission_dependency("user_session:view"))]
)
def get_user_sessions_by_user_id(
    user_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取指定用户的会话接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        session_service = UserSessionService(db)
        sessions = session_service.get_sessions_by_user_id(user_id, tenant_id=tenant_id)

        session_list = []
        for session in sessions:
            session_list.append({
                "id": session.id,
                "session_id": session.session_id,
                "device_type": session.device_type,
                "device_info": session.device_info,
                "ip_address": session.ip_address,
                "login_time": session.login_time.isoformat() if hasattr(session.login_time, 'isoformat') else session.login_time,
                "last_active_time": session.last_active_time.isoformat() if hasattr(session.last_active_time, 'isoformat') else session.last_active_time,
                "expire_time": session.expire_time.isoformat() if hasattr(session.expire_time, 'isoformat') else session.expire_time,
                "status": session.status
            })

        return ResponseUtils.success(
            data={
                "user_id": user_id,
                "total": len(session_list),
                "sessions": session_list
            },
            message="获取用户会话成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_user_sessions_by_user_id: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.get(
    "/{session_id}",
    response_model=AuthResponse,
    summary="获取会话详情",
    dependencies=[Depends(permission_dependency("user_session:view"))]
)
def get_user_session(
    session_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取会话详情接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        session_service = UserSessionService(db)
        session = session_service.get_session_by_id(session_id, tenant_id=tenant_id)

        session_info = {
            "id": session.id,
            "user_id": session.user_id,
            "session_id": session.session_id,
            "device_type": session.device_type,
            "device_info": session.device_info,
            "ip_address": session.ip_address,
            "login_time": session.login_time.isoformat() if hasattr(session.login_time, 'isoformat') else session.login_time,
            "last_active_time": session.last_active_time.isoformat() if hasattr(session.last_active_time, 'isoformat') else session.last_active_time,
            "expire_time": session.expire_time.isoformat() if hasattr(session.expire_time, 'isoformat') else session.expire_time,
            "status": session.status,
            "create_time": session.create_time.isoformat() if hasattr(session.create_time, 'isoformat') else session.create_time,
            "update_time": session.update_time.isoformat() if hasattr(session.update_time, 'isoformat') else session.update_time
        }

        return ResponseUtils.success(data=session_info, message="获取会话详情成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in get_user_session: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.delete(
    "/{session_id}",
    response_model=AuthResponse,
    summary="删除会话",
    dependencies=[Depends(permission_dependency("user_session:delete"))]
)
def delete_user_session(
    session_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """删除会话接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        session_service = UserSessionService(db)
        session_service.delete_session(session_id, tenant_id=tenant_id)

        return ResponseUtils.success(message="删除会话成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.post(
    "/kick",
    response_model=AuthResponse,
    summary="踢人下线",
    dependencies=[Depends(permission_dependency("user_session:update"))]
)
def kick_user(
    kick_data: KickUserRequest,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """踢人下线接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        session_service = UserSessionService(db)
        result = session_service.kick_user(kick_data.session_ids, tenant_id=tenant_id)

        return ResponseUtils.success(data=result, message="踢人下线成功")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in kick_user: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.post(
    "/kick-user/{user_id}",
    response_model=AuthResponse,
    summary="踢用户所有会话下线",
    dependencies=[Depends(permission_dependency("user_session:update"))]
)
def kick_all_user_sessions(
    user_id: int,
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """踢用户所有会话下线接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        session_service = UserSessionService(db)
        count = session_service.kick_all_user_sessions(user_id, tenant_id=tenant_id)

        return ResponseUtils.success(
            data={
                "user_id": user_id,
                "session_count": count
            },
            message="踢用户所有会话下线成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"Error in kick_all_user_sessions: {e}")
        print(traceback.format_exc())
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)


@router.post(
    "/clean-expired",
    response_model=AuthResponse,
    summary="清理过期会话",
    dependencies=[Depends(permission_dependency("user_session:delete"))]
)
def clean_expired_sessions(
    current_user_with_tenant = Depends(get_current_user_and_tenant_id),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """清理过期会话接口"""
    try:
        current_user, tenant_id = current_user_with_tenant
        session_service = UserSessionService(db)
        count = session_service.clean_expired_sessions(tenant_id=tenant_id)

        return ResponseUtils.success(
            data={"cleaned_count": count},
            message="清理过期会话成功"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseUtils.error(message=str(e), code=500, error_code=50000)
