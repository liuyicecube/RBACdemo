import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authService, userService, menuService } from '@/services'
import { storage } from '@/utils/storage'
import { sessionTimeout } from '@/utils/sessionTimeout'
import type { UserInfo, UserRole, Menu } from '@/types'
import { resetRouter } from '@/router'

export const useUserStore = defineStore('user', () => {
  const userInfo = ref<UserInfo | null>(null)
  const permissions = ref<string[]>([])
  const roles = ref<UserRole[]>([])
  const menus = ref<Menu[]>([])
  const currentSessionId = ref<string>('')

  const isLoggedIn = computed(() => !!userInfo.value && !!storage.getToken())

  const hasPermission = (permission: string): boolean => {
    return permissions.value.includes(permission)
  }

  const fetchUserInfo = async (): Promise<void> => {
    try {
      const [profile, perms, userRoles, menuTree] = await Promise.all([
        authService.getProfile(),
        userService.getCurrentUserPermissions(),
        userService.getCurrentUserRoles(),
        menuService.getUserMenuTree()
      ])
      
      userInfo.value = profile
      permissions.value = perms || []
      roles.value = userRoles || []
      menus.value = menuTree || []
    } catch (error) {
      console.error('[fetchUserInfo] 获取用户信息失败:', error)
      throw error
    }
  }

  const login = async (username: string, password: string): Promise<void> => {
    const result = await authService.login({ username, password })
    storage.setToken(result.accessToken)
    storage.setRefreshToken(result.refreshToken)
    if (result.sessionId) {
      currentSessionId.value = result.sessionId
      storage.setItem('sessionId', result.sessionId)
    }
    userInfo.value = result.user
    await fetchUserInfo()
    
    // 初始化会话超时
    sessionTimeout.updateLastActivity()
  }

  const logout = (): void => {
    // 清除会话超时定时器
    sessionTimeout.clearTimers()
    storage.clearAll()
    userInfo.value = null
    permissions.value = []
    roles.value = []
    menus.value = []
    currentSessionId.value = ''
    resetRouter()
  }

  // 初始化时恢复sessionId
  const initSessionId = () => {
    const savedSessionId = storage.getItem('sessionId')
    if (savedSessionId) {
      currentSessionId.value = savedSessionId
    }
  }

  initSessionId()

  return {
    userInfo,
    permissions,
    roles,
    menus,
    currentSessionId,
    isLoggedIn,
    hasPermission,
    fetchUserInfo,
    login,
    logout
  }
})
