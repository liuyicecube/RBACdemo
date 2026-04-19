import api from './api'
import type {
  UserInfo,
  UserListParams,
  UserCreateRequest,
  UserUpdateRequest,
  AssignRolesRequest,
  SetPrimaryRoleRequest,
  UserRole,
  PageResponse
} from '@/types'

export const userService = {
  getUsers: (params?: UserListParams): Promise<PageResponse<UserInfo>> => {
    return api.get('/users', { params })
  },

  getUser: (id: number): Promise<UserInfo> => {
    return api.get(`/users/${id}`)
  },

  createUser: (data: UserCreateRequest): Promise<UserInfo> => {
    return api.post('/users', data)
  },

  updateUser: (id: number, data: UserUpdateRequest): Promise<UserInfo> => {
    return api.put(`/users/${id}`, data)
  },

  deleteUser: (id: number): Promise<any> => {
    return api.delete(`/users/${id}`)
  },

  updateUserStatus: (id: number, status: number): Promise<any> => {
    return api.put(`/users/${id}/status`, null, { params: { status } })
  },

  uploadAvatar: (id: number, file: File): Promise<any> => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post(`/users/${id}/avatar`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  getUserRoles: (id: number): Promise<{ userId: number; roles: UserRole[] }> => {
    return api.get(`/users/${id}/roles`)
  },

  assignRoles: (id: number, data: AssignRolesRequest): Promise<any> => {
    return api.put(`/users/${id}/roles`, data)
  },

  setPrimaryRole: (id: number, data: SetPrimaryRoleRequest): Promise<any> => {
    return api.put(`/users/${id}/primary-role`, data)
  },

  getCurrentUserPermissions: (): Promise<string[]> => {
    return api.get('/users/me/permissions')
  },

  getCurrentUserRoles: (): Promise<UserRole[]> => {
    return api.get('/users/me/roles')
  },

  resetPassword: (data: { userId: number; newPassword: string }): Promise<any> => {
    return api.put(`/users/${data.userId}/reset-password`, data)
  }
}
