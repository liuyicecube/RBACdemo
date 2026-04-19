const ACCESS_TOKEN_KEY = 'access_token'
const REFRESH_TOKEN_KEY = 'refresh_token'

export const storage = {
  getToken: (): string | null => {
    return localStorage.getItem(ACCESS_TOKEN_KEY)
  },

  setToken: (token: string): void => {
    localStorage.setItem(ACCESS_TOKEN_KEY, token)
  },

  removeToken: (): void => {
    localStorage.removeItem(ACCESS_TOKEN_KEY)
  },

  getRefreshToken: (): string | null => {
    return localStorage.getItem(REFRESH_TOKEN_KEY)
  },

  setRefreshToken: (token: string): void => {
    localStorage.setItem(REFRESH_TOKEN_KEY, token)
  },

  removeRefreshToken: (): void => {
    localStorage.removeItem(REFRESH_TOKEN_KEY)
  },

  getItem: (key: string): string | null => {
    return localStorage.getItem(key)
  },

  setItem: (key: string, value: string): void => {
    localStorage.setItem(key, value)
  },

  removeItem: (key: string): void => {
    localStorage.removeItem(key)
  },

  clearAll: (): void => {
    localStorage.clear()
  }
}
