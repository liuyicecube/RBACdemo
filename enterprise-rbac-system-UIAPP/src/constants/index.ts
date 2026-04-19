export const STATUS_MAP = {
  ENABLED: 1,
  DISABLED: 0
} as const

export const STATUS_OPTIONS = [
  { value: STATUS_MAP.ENABLED, label: '启用', type: 'success' },
  { value: STATUS_MAP.DISABLED, label: '禁用', type: 'danger' }
] as const

export const MENU_TYPE_MAP = {
  DIRECTORY: 0,
  MENU: 1,
  BUTTON: 2
} as const

export const MENU_TYPE_OPTIONS = [
  { value: MENU_TYPE_MAP.DIRECTORY, label: '目录' },
  { value: MENU_TYPE_MAP.MENU, label: '菜单' },
  { value: MENU_TYPE_MAP.BUTTON, label: '按钮' }
] as const

export const PERMISSION_TYPE_MAP = {
  MENU: 1,
  BUTTON: 2
} as const

export const PERMISSION_TYPE_OPTIONS = [
  { value: PERMISSION_TYPE_MAP.MENU, label: '菜单' },
  { value: PERMISSION_TYPE_MAP.BUTTON, label: '按钮' }
] as const

export const PERMISSION_ACTION_OPTIONS = [
  { value: 'view', label: '查看' },
  { value: 'create', label: '创建' },
  { value: 'update', label: '更新' },
  { value: 'delete', label: '删除' }
] as const

export const DEFAULT_PAGE_SIZE = 10
export const PAGE_SIZE_OPTIONS = [10, 20, 50, 100]

export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'access_token',
  REFRESH_TOKEN: 'refresh_token',
  LANGUAGE: 'language',
  THEME: 'theme'
} as const

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1'

export const REGEX_PATTERNS = {
  USERNAME: /^[a-zA-Z0-9_]{5,20}$/,
  PASSWORD: /^.{6,}$/,
  EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  PHONE: /^1[3-9]\d{9}$/
} as const
