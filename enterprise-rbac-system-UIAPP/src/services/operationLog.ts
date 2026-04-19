import api from './api'
import type { PageResponse } from '@/types'

export interface OperationLogInfo {
  id: number
  user_id: number | null
  userId?: number | null
  username: string | null
  module: string
  operation: string
  description: string | null
  method: string | null
  requestMethod?: string | null
  url: string | null
  requestUrl?: string | null
  ip: string | null
  ipAddress?: string | null
  params: string | null
  requestParams?: string | null
  result: string | null
  responseResult?: string | null
  status: number
  error_msg: string | null
  errorMsg?: string | null
  execution_time: number | null
  executionTime?: number | null
  create_time: string
  createTime?: string
}

export interface OperationLogListParams {
  keyword?: string
  module?: string
  user_id?: number
  status?: number
  start_time?: string
  end_time?: string
  page?: number
  pageSize?: number
}

export const operationLogService = {
  getOperationLogs: (params?: OperationLogListParams): Promise<PageResponse<OperationLogInfo>> => {
    return api.get('/operation-logs', { params })
  },

  getOperationLog: (id: number): Promise<OperationLogInfo> => {
    return api.get(`/operation-logs/${id}`)
  },

  getStatistics: (days?: number): Promise<any> => {
    return api.get('/operation-logs/statistics', { params: { days } })
  },

  cleanupOldLogs: (days: number): Promise<any> => {
    return api.delete('/operation-logs/cleanup', { params: { days } })
  }
}
