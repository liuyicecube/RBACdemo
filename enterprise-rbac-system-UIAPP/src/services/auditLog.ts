import api from './api'
import type { PageResponse } from '@/types'

export interface AuditLogInfo {
  id: number
  user_id: number | null
  userId?: number | null
  username: string | null
  table_name: string
  tableName?: string
  record_id: number
  recordId?: number
  operation_type: string
  operationType?: string
  field_name: string | null
  fieldName?: string | null
  old_value: string | null
  oldValue?: string | null
  new_value: string | null
  newValue?: string | null
  change_reason: string | null
  changeReason?: string | null
  create_time: string
  createTime?: string
}

export interface AuditLogListParams {
  keyword?: string
  table_name?: string
  record_id?: number
  operation_type?: string
  user_id?: number
  start_time?: string
  end_time?: string
  page?: number
  pageSize?: number
}

export const auditLogService = {
  getAuditLogs: (params?: AuditLogListParams): Promise<PageResponse<AuditLogInfo>> => {
    return api.get('/audit-logs', { params })
  },

  getAuditLog: (id: number): Promise<AuditLogInfo> => {
    return api.get(`/audit-logs/${id}`)
  },

  getRecordChangeHistory: (table_name: string, record_id: number, page?: number, pageSize?: number): Promise<PageResponse<AuditLogInfo>> => {
    return api.get(`/audit-logs/record/${table_name}/${record_id}`, { params: { page, pageSize } })
  },

  getStatistics: (days?: number): Promise<any> => {
    return api.get('/audit-logs/statistics', { params: { days } })
  },

  cleanupOldLogs: (days: number): Promise<any> => {
    return api.delete('/audit-logs/cleanup', { params: { days } })
  }
}
