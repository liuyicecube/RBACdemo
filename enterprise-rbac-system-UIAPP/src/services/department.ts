import api from './api'
import type {
  Department,
  DepartmentListParams,
  DepartmentCreateRequest,
  PageResponse,
  UserInfo
} from '@/types'

export const departmentService = {
  getDepartments: (params?: DepartmentListParams): Promise<PageResponse<Department>> => {
    return api.get('/departments', { params })
  },

  getAllDepartments: (): Promise<Department[]> => {
    return api.get('/departments', { params: { page: 1, pageSize: 1000 } })
      .then((response: any) => response.items || [])
  },

  getDepartmentTree: (): Promise<Department[]> => {
    return api.get('/departments/tree')
  },

  getDepartment: (id: number): Promise<Department> => {
    return api.get(`/departments/${id}`)
  },

  createDepartment: (data: DepartmentCreateRequest): Promise<Department> => {
    return api.post('/departments', data)
  },

  updateDepartment: (id: number, data: Partial<DepartmentCreateRequest>): Promise<Department> => {
    return api.put(`/departments/${id}`, data)
  },

  deleteDepartment: (id: number): Promise<any> => {
    return api.delete(`/departments/${id}`)
  },

  updateDepartmentStatus: (id: number, status: number): Promise<any> => {
    return api.put(`/departments/${id}/status`, null, { params: { status } })
  },

  getDepartmentChildren: (id: number): Promise<Department[]> => {
    return api.get(`/departments/${id}/children`)
  },

  getDepartmentUsers: (id: number, params?: { page?: number; pageSize?: number }): Promise<PageResponse<UserInfo>> => {
    return api.get(`/departments/${id}/users`, { params })
  },

  getDepartmentUserCount: (id: number): Promise<number> => {
    return api.get(`/departments/${id}/user-count`)
  }
}
