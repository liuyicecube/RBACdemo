import api from './api'
import type {
  DataPermissionRule,
  DataPermissionRuleListParams,
  DataPermissionRuleCreateRequest,
  DataPermissionRuleUpdateRequest,
  PageResponse,
  RoleSimple
} from '@/types'

export const dataPermissionService = {
  getDataPermissionRules: (params?: DataPermissionRuleListParams): Promise<PageResponse<DataPermissionRule>> => {
    return api.get('/data-permission-rules', { params })
  },

  getAllActiveRules: (): Promise<DataPermissionRule[]> => {
    return api.get('/data-permission-rules/all')
  },

  getDataPermissionRule: (id: number): Promise<DataPermissionRule> => {
    return api.get(`/data-permission-rules/${id}`)
  },

  createDataPermissionRule: (data: DataPermissionRuleCreateRequest): Promise<DataPermissionRule> => {
    return api.post('/data-permission-rules', data)
  },

  updateDataPermissionRule: (id: number, data: Partial<DataPermissionRuleUpdateRequest>): Promise<DataPermissionRule> => {
    return api.put(`/data-permission-rules/${id}`, data)
  },

  deleteDataPermissionRule: (id: number): Promise<any> => {
    return api.delete(`/data-permission-rules/${id}`)
  },

  updateDataPermissionRuleStatus: (id: number, status: number): Promise<any> => {
    return api.put(`/data-permission-rules/${id}/status`, null, { params: { status } })
  },

  testDataPermissionRule: (id: number): Promise<any> => {
    return api.post(`/data-permission-rules/${id}/test`)
  }
}
