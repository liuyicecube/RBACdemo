import api from './api'
import type {
  Permission,
  PermissionListParams,
  PermissionCreateRequest,
  PageResponse,
  RoleSimple
} from '@/types'

export const permissionService = {
  getPermissions: (params?: PermissionListParams): Promise<PageResponse<Permission>> => {
    return api.get('/permissions', { params })
  },

  getAllPermissions: (): Promise<Permission[]> => {
    return api.get('/permissions/all')
  },

  getPermission: (id: number): Promise<Permission> => {
    return api.get(`/permissions/${id}`)
  },

  createPermission: (data: PermissionCreateRequest): Promise<Permission> => {
    return api.post('/permissions', data)
  },

  updatePermission: (id: number, data: Partial<PermissionCreateRequest>): Promise<Permission> => {
    return api.put(`/permissions/${id}`, data)
  },

  deletePermission: (id: number): Promise<any> => {
    return api.delete(`/permissions/${id}`)
  },

  batchCreatePermissions: (data: PermissionCreateRequest[]): Promise<Permission[]> => {
    return api.post('/permissions/batch', data)
  },

  batchDeletePermissions: (permissionIds: number[]): Promise<any> => {
    return api.delete('/permissions/batch', { params: { permissionIds } })
  },

  updatePermissionStatus: (id: number, status: number): Promise<any> => {
    return api.put(`/permissions/${id}/status`, null, { params: { status } })
  },

  getPermissionRoles: (id: number): Promise<{ permissionId: number; roles: RoleSimple[] }> => {
    return api.get(`/permissions/${id}/roles`)
  },

  countPermissionRoles: (id: number): Promise<{ permissionId: number; roleCount: number }> => {
    return api.get(`/permissions/${id}/role-count`)
  }
}
