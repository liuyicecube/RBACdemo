"""Cache Warmup"""

from App.Config.Database import SessionLocal
from App.Repositories.UserRepository import UserRepository
from App.Repositories.RoleRepository import RoleRepository
from App.Repositories.DepartmentRepository import DepartmentRepository
from App.Repositories.MenuRepository import MenuRepository
from App.Repositories.PermissionRepository import PermissionRepository
from App.Utils.Cache import cache


def warmup_cache():
    """预热缓存"""
    print("开始执行缓存预热...")

    try:
        # 创建数据库会话
        db = SessionLocal()
    except Exception:
        print("缓存预热跳过: 无法连接数据库")
        return

    try:
        # 1. 预热用户列表
        user_repo = UserRepository(db)
        users = user_repo.get_all()
        users_data = [{"id": user.id, "username": user.username, "nickname": user.nickname} for user in users]
        cache.set_json("users:list", users_data, expire=3600)
        print(f"用户列表缓存预热完成，共{len(users_data)}个用户")

        # 2. 预热角色列表
        role_repo = RoleRepository(db)
        roles = role_repo.get_all()
        roles_data = [{"id": role.id, "name": role.name, "code": role.code} for role in roles]
        cache.set_json("roles:list", roles_data, expire=3600)
        print(f"角色列表缓存预热完成，共{len(roles_data)}个角色")

        # 3. 预热部门列表
        dept_repo = DepartmentRepository(db)
        depts = dept_repo.get_all()
        depts_data = [{"id": dept.id, "name": dept.name, "code": dept.code} for dept in depts]
        cache.set_json("departments:list", depts_data, expire=3600)
        print(f"部门列表缓存预热完成，共{len(depts_data)}个部门")

        # 4. 预热菜单列表
        menu_repo = MenuRepository(db)
        menus = menu_repo.get_all()
        menus_data = [{"id": menu.id, "name": menu.name, "code": menu.code, "path": menu.path} for menu in menus]
        cache.set_json("menus:list", menus_data, expire=3600)
        print(f"菜单列表缓存预热完成，共{len(menus_data)}个菜单")

        # 5. 预热权限列表
        perm_repo = PermissionRepository(db)
        permissions = perm_repo.get_all()
        permissions_data = [{"id": perm.id, "name": perm.name, "code": perm.code, "path": perm.path} for perm in permissions]
        cache.set_json("permissions:list", permissions_data, expire=3600)
        print(f"权限列表缓存预热完成，共{len(permissions_data)}个权限")

        # 6. 预热活跃权限列表
        active_permissions = perm_repo.get_active_permissions()
        active_permissions_data = [{"id": perm.id, "name": perm.name, "code": perm.code, "path": perm.path} for perm in active_permissions]
        cache.set_json("permissions:active", active_permissions_data, expire=3600)
        print(f"活跃权限列表缓存预热完成，共{len(active_permissions_data)}个活跃权限")

        print("缓存预热完成！")
    except Exception as e:
        print(f"缓存预热跳过: {type(e).__name__}")
    finally:
        # 关闭数据库会话
        try:
            db.close()
        except Exception:
            pass
