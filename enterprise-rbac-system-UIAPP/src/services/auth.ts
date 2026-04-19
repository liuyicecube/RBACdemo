import api from './api'
import type {
  LoginRequest,
  LoginResponse,
  RefreshTokenRequest,
  RefreshTokenResponse,
  ChangePasswordRequest,
  ResetPasswordRequest,
  UserInfo
} from '@/types'

export const authService = {
  login: (data: LoginRequest): Promise<LoginResponse> => {
    return api.post('/auth/login', data)
  },

  register: (data: any): Promise<any> => {
    return api.post('/auth/register', data)
  },

  refreshToken: (data: RefreshTokenRequest): Promise<RefreshTokenResponse> => {
    return api.post('/auth/refresh', data)
  },

  changePassword: (data: ChangePasswordRequest): Promise<any> => {
    return api.post('/auth/change-password', data)
  },

  resetPassword: (data: ResetPasswordRequest): Promise<any> => {
    return api.post('/auth/reset-password', data)
  },

  getProfile: (): Promise<UserInfo> => {
    return api.get('/auth/profile')
  },

  logout: (): Promise<any> => {
    return api.post('/auth/logout')
  }
}
