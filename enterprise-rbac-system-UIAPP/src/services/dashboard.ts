import api from './api'

export interface DashboardStats {
  userCount: number
  roleCount: number
  permissionCount: number
  departmentCount: number
  operationLogCount: number
  activeUserCount: number
}

export interface CacheMetrics {
  hitCount: number
  missCount: number
  totalRequests: number
  hitRate: number
}

export const dashboardService = {
  getDashboardStats: (): Promise<DashboardStats> => {
    return api.get('/dashboard/stats')
  },

  getCacheMetrics: (): Promise<CacheMetrics> => {
    return api.get('/metrics/cache')
  },

  resetCacheMetrics: (): Promise<any> => {
    return api.get('/metrics/cache/reset')
  }
}
