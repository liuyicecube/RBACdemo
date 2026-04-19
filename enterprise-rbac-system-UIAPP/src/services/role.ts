import api from './api'
import type {
  Role,
  RoleSimple,
  RoleListParams,
  RoleCreateRequest,
  RoleUpdateRequest,
  AssignPermissionsRequest,
  PageResponse,
  UserInfo
} from '@/types'

export const roleService = {
  getRoles: (params?: RoleListParams): Promise<PageResponse<Role>> => {
    return api.get('/roles', { params })
  },

  getAllRoles: (): Promise<RoleSimple[]> => {
    return api.get('/roles/all')
  },

  getRole: (id: number): Promise<Role> => {
    return api.get(`/roles/${id}`)
  },

  createRole: (data: RoleCreateRequest): Promise<Role> => {
    return api.post('/roles', data)
  },

  updateRole: (id: number, data: RoleUpdateRequest): Promise<Role> => {
    return api.put(`/roles/${id}`, data)
  },

  deleteRole: (id: number): Promise<any> => {
    return api.delete(`/roles/${id}`)
  },

  updateRoleStatus: (id: number, status: number): Promise<any> => {
    return api.put(`/roles/${id}/status`, null, { params: { status } })
  },

  getRolePermissions: (id: number): Promise<any[]> => {
    return api.get(`/roles/${id}/permissions`)
  },

  assignPermissions: (id: number, data: AssignPermissionsRequest): Promise<any> => {
    return api.put(`/roles/${id}/permissions`, data)
  },

  getRoleUsers: (id: number): Promise<UserInfo[]> => {
    return api.get(`/roles/${id}/users`)
  }
}
