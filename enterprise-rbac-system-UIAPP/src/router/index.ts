import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { useUserStore, useTabsStore } from '@/store'
import { ElMessage } from 'element-plus'
import { generateRoutesFromMenus } from '@/utils/routerUtils'
import { sessionTimeout } from '@/utils/sessionTimeout'

let dynamicRoutesAdded = false
let addedRouteNames: string[] = []
let isReloading = false

// 临时加载组件 - 只是简单显示加载状态，避免页面跳转
const TemporaryLoadComponent = {
  template: '<div style="display:flex;align-items:center;justify-content:center;height:100vh;"><div>加载中...</div></div>'
}

// 初始路由配置 - 在 Layout 下添加临时通配符路由，避免警告，同时确保能停留在当前路径
const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/LoginPage.vue'),
    meta: { requiresAuth: false, title: '登录' }
  },
  {
    path: '/',
    name: 'Layout',
    component: () => import('@/components/layout/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Home',
        redirect: '/dashboard'
      },
      // 临时通配符路由 - 捕获所有路径，避免刷新时的警告
      {
        path: ':pathMatch(.*)*',
        name: 'TemporaryCatchAll',
        component: TemporaryLoadComponent,
        meta: { requiresAuth: true }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export const resetRouter = () => {
  dynamicRoutesAdded = false
  addedRouteNames.forEach(name => {
    if (router.hasRoute(name)) {
      router.removeRoute(name)
    }
  })
  addedRouteNames = []
  
  // 移除 NotFound 路由（如果存在）
  if (router.hasRoute('NotFound')) {
    router.removeRoute('NotFound')
  }
  
  // 重新添加临时通配符路由到 Layout 下（如果不存在）
  if (!router.hasRoute('TemporaryCatchAll')) {
    router.addRoute('Layout', {
      path: ':pathMatch(.*)*',
      name: 'TemporaryCatchAll',
      component: TemporaryLoadComponent,
      meta: { requiresAuth: true }
    })
  }
}

// 添加 404 路由并替换临时路由
const add404Route = () => {
  // 移除临时通配符路由（在 Layout 下）
  if (router.hasRoute('TemporaryCatchAll')) {
    router.removeRoute('TemporaryCatchAll')
  }
  
  // 添加全局的 404 路由
  if (!router.hasRoute('NotFound')) {
    router.addRoute({
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('@/views/error/NotFoundPage.vue'),
      meta: { requiresAuth: false, title: '404' }
    })
  }
}

router.beforeEach(async (to, _from, next) => {
  const userStore = useUserStore()
  const hasToken = !!useUserStore().isLoggedIn || !!window.localStorage.getItem('access_token')
  
  // 只有明确设置了 requiresAuth: false 的才不需要认证
  const isLoginPage = to.name === 'Login' || to.path === '/login'
  const requiresAuth = !isLoginPage

  if (requiresAuth && !hasToken) {
    sessionTimeout.clearTimers()
    next({ name: 'Login' })
    return
  }

  if (!requiresAuth && hasToken && to.name === 'Login') {
    next({ name: 'Dashboard' })
    return
  }

  if (requiresAuth && hasToken) {
    // 初始化会话超时
    sessionTimeout.init()
    
    // 检查是否需要加载用户信息
    if (!userStore.userInfo || userStore.permissions.length === 0) {
      try {
        await userStore.fetchUserInfo()
      } catch (error) {
        userStore.logout()
        resetRouter()
        next({ name: 'Login' })
        return
      }
    }

    // 检查是否需要添加动态路由
    if (!dynamicRoutesAdded && userStore.menus && userStore.menus.length > 0) {
      try {
        const dynamicRoutes = generateRoutesFromMenus(userStore.menus)
        
        // 为每个动态路由添加到主布局下
        dynamicRoutes.forEach(route => {
          const routeName = route.name as string
          if (!router.hasRoute(routeName)) {
            router.addRoute('Layout', route)
            addedRouteNames.push(routeName)
          }
        })
        
        // 替换临时通配符路由为真实的 404 路由
        add404Route()
        
        dynamicRoutesAdded = true
        isReloading = true
        
        // 重导航到目标路径，确保停留在当前页面
        next({ path: to.fullPath, replace: true })
        return
      } catch (error) {
        console.error('Failed to add dynamic routes:', error)
      }
    }

    // 只有明确设置了 permission 且权限格式正确时才检查
    if (to.meta.permission) {
      const permission = to.meta.permission as string
      // 只检查包含冒号的权限格式（如 user:view）
      if (permission.includes(':') && !userStore.hasPermission(permission)) {
        ElMessage.error('您没有访问该页面的权限')
        next({ name: 'Dashboard' })
        return
      }
    }
  }

  next()
})

router.afterEach((to) => {
  if (to.meta.requiresAuth !== false && to.name !== 'Login') {
    const tabsStore = useTabsStore()
    tabsStore.addTab(to)
  }
})

export default router
