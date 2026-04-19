import api from './api'
import axios from 'axios'
import { storage } from '@/utils/storage'

const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1'

export interface SystemConfig {
  id: number
  configKey: string
  configValue: string
  configType: string
  groupName: string
  isSystem: number
  description: string
  sort: number
  status: number
  createTime: string
  updateTime: string
}

export interface PaginationParams {
  keyword?: string
  groupName?: string
  status?: number
  page?: number
  pageSize?: number
}

export interface ConfigCreate {
  configKey: string
  configValue?: string
  configType?: string
  description?: string
  groupName?: string
  isSystem?: number
  sort?: number
  status?: number
}

export interface ConfigUpdate {
  configValue?: string
  configType?: string
  description?: string
  groupName?: string
  isSystem?: number
  sort?: number
  status?: number
}

const systemConfigService = {
  getConfigs: (params?: PaginationParams): Promise<any> => {
    return api.get('/system-configs', { params })
  },

  getConfigGroups: (): Promise<any> => {
    return api.get('/system-configs/groups')
  },

  getGroupedConfigs: (): Promise<any> => {
    return api.get('/system-configs/grouped')
  },

  getActiveConfigs: (): Promise<any> => {
    return api.get('/system-configs/active')
  },

  getConfig: (configId: number): Promise<any> => {
    return api.get(`/system-configs/${configId}`)
  },

  getConfigByKey: (key: string): Promise<any> => {
    return api.get(`/system-configs/key/${key}`)
  },

  createConfig: (data: ConfigCreate): Promise<any> => {
    return api.post('/system-configs', data)
  },

  updateConfig: (configId: number, data: ConfigUpdate): Promise<any> => {
    return api.put(`/system-configs/${configId}`, data)
  },

  deleteConfig: (configId: number): Promise<any> => {
    return api.delete(`/system-configs/${configId}`)
  },

  batchUpdateConfigs: async (configs: Record<string, any>): Promise<any> => {
    const token = storage.getToken()
    const response = await fetch(`${BASE_URL}/system-configs/batch-update`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {})
      },
      body: JSON.stringify(configs)
    })
    
    const data = await response.json()
    if (data.code === 200 || data.code === 0) {
      return data.data
    } else {
      throw new Error(data.message || '请求失败')
    }
  },

  refreshCache: (): Promise<any> => {
    return api.post('/system-configs/refresh-cache')
  }
}

export default systemConfigService
