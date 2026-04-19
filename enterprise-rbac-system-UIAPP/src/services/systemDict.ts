import api from './api'

export interface SystemDict {
  id: number
  name: string
  code: string
  description?: string
  sort: number
  status: number
  createTime: string
  updateTime: string
}

export interface SystemDictItem {
  id: number
  dictId: number
  label: string
  value: string | number
  sort: number
  description?: string
  status: number
  createTime: string
  updateTime: string
}

export interface DictItemSimple {
  label: string
  value: string | number
  sort: number
}

export interface PaginationParams {
  keyword?: string
  status?: number
  page?: number
  pageSize?: number
}

export interface DictCreate {
  name: string
  code: string
  description?: string
  sort?: number
  status?: number
}

export interface DictUpdate {
  name?: string
  description?: string
  sort?: number
  status?: number
}

export interface DictItemCreate {
  label: string
  value: string | number
  sort?: number
  description?: string
  status?: number
}

export interface DictItemUpdate {
  label?: string
  value?: string | number
  sort?: number
  description?: string
  status?: number
}

export const systemDictService = {
  getDicts: (params?: PaginationParams): Promise<any> => {
    return api.get('/system-dicts', { params })
  },

  getActiveDicts: (): Promise<any> => {
    return api.get('/system-dicts/active')
  },

  getDict: (dictId: number): Promise<any> => {
    return api.get(`/system-dicts/${dictId}`)
  },

  getDictItemsByCode: (code: string): Promise<DictItemSimple[]> => {
    return api.get(`/system-dicts/code/${code}`)
  },

  getDictItems: (dictId: number): Promise<any> => {
    return api.get(`/system-dicts/${dictId}/items`)
  },

  createDict: (data: DictCreate): Promise<any> => {
    return api.post('/system-dicts', data)
  },

  updateDict: (dictId: number, data: DictUpdate): Promise<any> => {
    return api.put(`/system-dicts/${dictId}`, data)
  },

  deleteDict: (dictId: number): Promise<any> => {
    return api.delete(`/system-dicts/${dictId}`)
  },

  createDictItem: (dictId: number, data: DictItemCreate): Promise<any> => {
    return api.post(`/system-dicts/${dictId}/items`, data)
  },

  updateDictItem: (itemId: number, data: DictItemUpdate): Promise<any> => {
    return api.put(`/system-dicts/items/${itemId}`, data)
  },

  deleteDictItem: (itemId: number): Promise<any> => {
    return api.delete(`/system-dicts/items/${itemId}`)
  }
}
