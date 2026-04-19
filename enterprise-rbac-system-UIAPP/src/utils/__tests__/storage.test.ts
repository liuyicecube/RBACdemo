import { describe, it, expect, beforeEach, vi } from 'vitest'
import { storage } from '../storage'

describe('storage utility', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.clearAllMocks()
  })

  describe('token operations', () => {
    it('should set and get token', () => {
      const testToken = 'test-token-123'
      storage.setToken(testToken)
      expect(storage.getToken()).toBe(testToken)
    })

    it('should return null when token not found', () => {
      expect(storage.getToken()).toBeNull()
    })

    it('should remove token', () => {
      storage.setToken('test-token')
      storage.removeToken()
      expect(storage.getToken()).toBeNull()
    })
  })

  describe('refresh token operations', () => {
    it('should set and get refresh token', () => {
      const testRefreshToken = 'test-refresh-token-123'
      storage.setRefreshToken(testRefreshToken)
      expect(storage.getRefreshToken()).toBe(testRefreshToken)
    })

    it('should remove refresh token', () => {
      storage.setRefreshToken('test-refresh-token')
      storage.removeRefreshToken()
      expect(storage.getRefreshToken()).toBeNull()
    })
  })

  describe('user info operations', () => {
    it('should set and get user info', () => {
      const userInfo = { id: 1, username: 'testuser' }
      storage.setUserInfo(userInfo)
      expect(storage.getUserInfo()).toEqual(userInfo)
    })

    it('should remove user info', () => {
      storage.setUserInfo({ id: 1 })
      storage.removeUserInfo()
      expect(storage.getUserInfo()).toBeNull()
    })
  })

  describe('clear all', () => {
    it('should clear all storage items', () => {
      storage.setToken('token')
      storage.setRefreshToken('refresh-token')
      storage.setUserInfo({ id: 1 })
      storage.clearAll()
      expect(storage.getToken()).toBeNull()
      expect(storage.getRefreshToken()).toBeNull()
      expect(storage.getUserInfo()).toBeNull()
    })
  })
})
