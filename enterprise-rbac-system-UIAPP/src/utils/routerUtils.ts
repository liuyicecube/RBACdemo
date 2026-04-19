import type { RouteRecordRaw } from 'vue-router'
import type { Menu } from '@/types'

const componentMap: Record<string, any> = {
  'dashboard/DashboardPage': () => import('@/views/dashboard/DashboardPage.vue'),
  'users/UserListPage': () => import('@/views/users/UserListPage.vue'),
  'roles/RoleListPage': () => import('@/views/roles/RoleListPage.vue'),
  'permissions/PermissionListPage': () => import('@/views/permissions/PermissionListPage.vue'),
  'menus/MenuListPage': () => import('@/views/menus/MenuListPage.vue'),
  'departments/DepartmentListPage': () => import('@/views/departments/DepartmentListPage.vue'),
  'auth/ProfilePage': () => import('@/views/auth/ProfilePage.vue'),
  'logs/OperationLogPage': () => import('@/views/logs/OperationLogPage.vue'),
  'logs/AuditLogPage': () => import('@/views/logs/AuditLogPage.vue'),
  'dictionaries/DictionaryListPage': () => import('@/views/dictionaries/DictionaryListPage.vue'),
  'settings/SystemSettingsPage': () => import('@/views/settings/SystemSettingsPage.vue'),
  'dataPermissions/DataPermissionListPage': () => import('@/views/dataPermissions/DataPermissionListPage.vue'),
  'sessions/SessionListPage': () => import('@/views/sessions/SessionListPage.vue')
}

export const loadComponent = (componentPath: string | undefined): any => {
  if (!componentPath) {
    return null
  }
  
  if (componentMap[componentPath]) {
    return componentMap[componentPath]
  }
  
  try {
    return () => import(`@/views/${componentPath}.vue`)
  } catch {
    console.warn(`Component not found: ${componentPath}`)
    return null
  }
}

const flattenMenus = (menus: Menu[]): Menu[] => {
  const result: Menu[] = []
  
  const flatten = (items: Menu[]) => {
    items.forEach(item => {
      result.push(item)
      if (item.children && item.children.length > 0) {
        flatten(item.children)
      }
    })
  }
  
  flatten(menus)
  return result
}

export const transformMenuToRoute = (menu: Menu): RouteRecordRaw | null => {
  const component = loadComponent(menu.component)
  
  if (!component) {
    return null
  }
  
  const ensureRelativePath = (path: string | undefined): string => {
    if (!path) return ''
    // 确保路径是相对路径（去掉开头的 /）
    if (path.startsWith('/')) {
      return path.substring(1)
    }
    return path
  }
  
  const route: RouteRecordRaw = {
    path: ensureRelativePath(menu.path),
    name: menu.code || `menu_${menu.id}`,
    component: component,
    meta: {
      title: menu.name,
      icon: menu.icon,
      requiresAuth: true
    }
  }
  
  return route
}

export const generateRoutesFromMenus = (menus: Menu[]): RouteRecordRaw[] => {
  const allMenus = flattenMenus(menus)
  
  const result = allMenus
    .filter(menu => menu.type === 1)
    .map(transformMenuToRoute)
    .filter((route): route is RouteRecordRaw => route !== null)
  
  return result
}
