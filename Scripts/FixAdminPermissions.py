"""
修复admin用户权限配置脚本
功能：为admin用户添加缺少的权限
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from App.Config.Database import SessionLocal
from App.Models.Permission import PermissionModel
from App.Models.Role import RoleModel
from App.Models.RolePermission import RolePermissionModel
from App.Models.UserRole import UserRoleModel
from App.Models.User import UserModel


def fix_admin_permissions(db):
    """修复admin用户权限"""
    print("正在检查和修复admin用户权限...")
    
    # 查找admin用户
    admin_user = db.query(UserModel).filter(UserModel.username == "admin", UserModel.tenant_id == 1).first()
    if not admin_user:
        print("[FAIL] 未找到admin用户")
        return
    
    print(f"[OK] 找到admin用户: {admin_user.username} (ID: {admin_user.id})")
    
    # 查找admin用户的角色
    user_roles = db.query(UserRoleModel).filter(UserRoleModel.user_id == admin_user.id, UserRoleModel.tenant_id == 1).all()
    
    if not user_roles:
        print("[FAIL] admin用户没有分配角色")
        return
    
    # 获取所有角色
    role_ids = [ur.role_id for ur in user_roles]
    roles = db.query(RoleModel).filter(RoleModel.id.in_(role_ids), RoleModel.tenant_id == 1).all()
    
    for role in roles:
        print(f"[OK] admin用户拥有角色: {role.name} (code: {role.code})")
    
    # 确保所有权限都存在，如果不存在则创建
    required_permissions = [
        {"name": "权限查看", "code": "permission:view", "type": 2, "resource_type": "permission", "action": "view", "path": "/api/v1/permissions", "method": "GET"},
        {"name": "权限创建", "code": "permission:create", "type": 2, "resource_type": "permission", "action": "create", "path": "/api/v1/permissions", "method": "POST"},
        {"name": "权限更新", "code": "permission:update", "type": 2, "resource_type": "permission", "action": "update", "path": "/api/v1/permissions/*", "method": "PUT"},
        {"name": "权限删除", "code": "permission:delete", "type": 2, "resource_type": "permission", "action": "delete", "path": "/api/v1/permissions/*", "method": "DELETE"},
        {"name": "审计日志查看", "code": "audit:view", "type": 2, "resource_type": "audit", "action": "view", "path": "/api/v1/audit-logs", "method": "GET"},
        {"name": "用户组查看", "code": "user_group:view", "type": 2, "resource_type": "user_group", "action": "view", "path": "/api/v1/user-groups", "method": "GET"},
        {"name": "用户组创建", "code": "user_group:create", "type": 2, "resource_type": "user_group", "action": "create", "path": "/api/v1/user-groups", "method": "POST"},
        {"name": "用户组更新", "code": "user_group:update", "type": 2, "resource_type": "user_group", "action": "update", "path": "/api/v1/user-groups/*", "method": "PUT"},
        {"name": "用户组删除", "code": "user_group:delete", "type": 2, "resource_type": "user_group", "action": "delete", "path": "/api/v1/user-groups/*", "method": "DELETE"}
    ]
    
    for perm_data in required_permissions:
        existing_perm = db.query(PermissionModel).filter(
            PermissionModel.code == perm_data["code"],
            PermissionModel.tenant_id == 1
        ).first()
        
        if not existing_perm:
            perm = PermissionModel(
                name=perm_data["name"],
                code=perm_data["code"],
                type=perm_data["type"],
                resource_type=perm_data["resource_type"],
                action=perm_data["action"],
                path=perm_data.get("path"),
                method=perm_data.get("method"),
                level=1,
                tenant_id=1,
                status=1
            )
            db.add(perm)
            print(f"[OK] 创建缺失权限: {perm_data['code']}")
    
    db.commit()
    
    # 获取所有权限
    all_permissions = db.query(PermissionModel).filter(PermissionModel.tenant_id == 1).all()
    print(f"[OK] 系统共有 {len(all_permissions)} 个权限")
    
    # 为admin用户的角色分配所有权限
    for role in roles:
        # 先检查角色已有权限
        existing_role_perms = db.query(RolePermissionModel).filter(
            RolePermissionModel.role_id == role.id,
            RolePermissionModel.tenant_id == 1
        ).all()
        existing_perm_ids = {rp.permission_id for rp in existing_role_perms}
        
        # 分配所有缺失的权限
        for perm in all_permissions:
            if perm.id not in existing_perm_ids:
                role_perm = RolePermissionModel(
                    role_id=role.id,
                    permission_id=perm.id,
                    tenant_id=1
                )
                db.add(role_perm)
                print(f"[OK] 为角色 {role.name} 添加权限: {perm.code}")
        
        db.commit()
        print(f"[OK] 角色 {role.name} 权限分配完成")
    
    print("\n[OK] admin用户权限修复完成！")


def main():
    print("=" * 60)
    print("修复admin用户权限配置脚本")
    print("=" * 60)
    
    db = SessionLocal()
    try:
        fix_admin_permissions(db)
    except Exception as e:
        print(f"\n[FAIL] 修复失败: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
