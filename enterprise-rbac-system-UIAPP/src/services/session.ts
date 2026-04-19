import api from './api'
import type { PageResponse, SessionInfo } from '@/types'

export interface SessionListParams {
  user_id?: number
  device_type?: string
  status?: number
  keyword?: string
  page?: number
  page_size?: number
}

export interface KickUserRequest {
  session_ids: number[]
}

export const sessionService = {
  getSessions: (params?: SessionListParams): Promise<PageResponse<SessionInfo>> => {
    return api.get('/user-sessions', { params })
  },

  getSession: (id: number): Promise<SessionInfo> => {
    return api.get(`/user-sessions/${id}`)
  },

  getOnlineSessions: (): Promise<{ total: number; sessions: SessionInfo[] }> => {
    return api.get('/user-sessions/online')
  },

  getUserSessions: (userId: number): Promise<{ user_id: number; total: number; sessions: SessionInfo[] }> => {
    return api.get(`/user-sessions/user/${userId}`)
  },

  deleteSession: (id: number): Promise<any> => {
    return api.delete(`/user-sessions/${id}`)
  },

  kickUser: (data: KickUserRequest): Promise<{ success_count: number; failed_count: number }> => {
    return api.post('/user-sessions/kick', data)
  },

  kickAllUserSessions: (userId: number): Promise<{ user_id: number; session_count: number }> => {
    return api.post(`/user-sessions/kick-user/${userId}`)
  },

  countExpiredSessions: (): Promise<{ expired_count: number; expired_status_count: number; total_to_clean: number }> => {
    return api.get('/user-sessions/count-expired')
  },

  cleanExpiredSessions: (): Promise<{ expired_count: number; expired_status_count: number; total_cleaned: number }> => {
    return api.post('/user-sessions/clean-expired')
  }
}
