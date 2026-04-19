import api from './api'
import type {
  Menu,
  MenuListParams,
  MenuCreateRequest,
  SortMenusRequest,
  PageResponse
} from '@/types'

export const menuService = {
  getMenus: (params?: MenuListParams): Promise<PageResponse<Menu>> => {
    return api.get('/menus', { params })
  },

  getMenuTree: (): Promise<Menu[]> => {
    return api.get('/menus/tree')
  },

  getUserMenuTree: (): Promise<Menu[]> => {
    return api.get('/menus/user')
  },

  getMenu: (id: number): Promise<Menu> => {
    return api.get(`/menus/${id}`)
  },

  createMenu: (data: MenuCreateRequest): Promise<Menu> => {
    return api.post('/menus', data)
  },

  updateMenu: (id: number, data: Partial<MenuCreateRequest>): Promise<Menu> => {
    return api.put(`/menus/${id}`, data)
  },

  deleteMenu: (id: number): Promise<any> => {
    return api.delete(`/menus/${id}`)
  },

  sortMenus: (data: SortMenusRequest): Promise<any> => {
    return api.put('/menus/sort', data)
  },

  updateMenuStatus: (id: number, status: number): Promise<any> => {
    return api.put(`/menus/${id}/status`, null, { params: { status } })
  },

  getMenuChildren: (id: number): Promise<Menu[]> => {
    return api.get(`/menus/${id}/children`)
  }
}
