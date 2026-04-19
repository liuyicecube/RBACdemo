import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useUserStore } from '../modules/user'

describe('User Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should initialize with default values', () => {
    const store = useUserStore()
    expect(store.token).toBeNull()
    expect(store.userInfo).toBeNull()
    expect(store.isLoggedIn).toBe(false)
  })

  it('should set token', () => {
    const store = useUserStore()
    store.setToken('test-token-123')
    expect(store.token).toBe('test-token-123')
  })

  it('should set user info', () => {
    const store = useUserStore()
    const userInfo = { id: 1, username: 'testuser', email: 'test@example.com' }
    store.setUserInfo(userInfo)
    expect(store.userInfo).toEqual(userInfo)
  })

  it('should update isLoggedIn when token is set', () => {
    const store = useUserStore()
    expect(store.isLoggedIn).toBe(false)
    store.setToken('test-token')
    expect(store.isLoggedIn).toBe(true)
  })

  it('should clear user data on logout', () => {
    const store = useUserStore()
    store.setToken('test-token')
    store.setUserInfo({ id: 1 })
    store.logout()
    expect(store.token).toBeNull()
    expect(store.userInfo).toBeNull()
    expect(store.isLoggedIn).toBe(false)
  })
})
