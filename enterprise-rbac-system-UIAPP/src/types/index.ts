export interface UserInfo {
  id: number
  username: string
  nickname: string
  email?: string
  phone?: string
  avatar?: string
  departmentId?: number
  tenantId?: number
  status: number
  lastLoginTime?: string
  lastLoginIp?: string
  createTime?: string
  updateTime?: string
}

export interface UserRole {
  id: number
  name: string
  code: string
  type: number
  isPrimary: boolean
}

export interface UserListParams {
  keyword?: string
  departmentId?: number
  status?: number
  page?: number
  pageSize?: number
}

export interface UserCreateRequest {
  username: string
  password: string
  nickname: string
  email?: string
  phone?: string
  avatar?: string
  departmentId?: number
  status?: number
}

export interface UserUpdateRequest {
  nickname?: string
  email?: string
  phone?: string
  avatar?: string
  departmentId?: number
  status?: number
  password?: string
}

export interface Role {
  id: number
  name: string
  code: string
  description?: string
  sort: number
  sort_order?: number
  status: number
  type?: number
  data_scope?: number
  dataScope?: number
  parent_id?: number
  parentId?: number
  icon?: string
  color?: string
  createTime: string
  updateTime: string
}

export interface RoleSimple {
  id: number
  name: string
  code: string
  status: number
  description?: string
}

export interface RoleListParams {
  keyword?: string
  status?: number
  page?: number
  pageSize?: number
}

export interface RoleCreateRequest {
  name: string
  code: string
  description?: string
  sort?: number
  status?: number
  type?: number
  data_scope?: number
  parent_id?: number
  icon?: string
  color?: string
}

export interface RoleUpdateRequest {
  name?: string
  code?: string
  description?: string
  sort?: number
  status?: number
  type?: number
  data_scope?: number
  parent_id?: number
  icon?: string
  color?: string
}

export interface Permission {
  id: number
  name: string
  code: string
  type: number
  resourceType?: string
  resourceId?: string | number
  action?: string
  path?: string
  method?: string
  parentId?: number
  level: number
  status: number
  description?: string
  icon?: string
  color?: string
  createTime: string
  updateTime: string
  children?: Permission[]
}

export interface PermissionListParams {
  keyword?: string
  type?: number
  resourceType?: string
  action?: string
  status?: number
  parentId?: number
  page?: number
  pageSize?: number
}

export interface PermissionCreateRequest {
  name: string
  code: string
  type: number
  resourceType: string
  resourceId?: string | number
  action: string
  path?: string
  method?: string
  parentId?: number
  description?: string
  status?: number
  icon?: string
  color?: string
}

export interface Menu {
  id: number
  name: string
  code: string
  parentId?: number
  level: number
  type: number
  path?: string
  component?: string
  icon?: string
  sort: number
  status: number
  createTime: string
  updateTime: string
  children?: Menu[]
}

export interface MenuListParams {
  keyword?: string
  type?: number
  status?: number
  parentId?: number
  page?: number
  pageSize?: number
}

export interface MenuCreateRequest {
  name: string
  code: string
  parentId?: number
  type: number
  path?: string
  component?: string
  icon?: string
  sort?: number
  status?: number
}

export interface Department {
  id: number
  name: string
  code: string
  parentId?: number
  level: number
  leaderId?: number
  contactPhone?: string
  address?: string
  description?: string
  status: number
  createTime: string
  updateTime: string
  children?: Department[]
}

export interface DepartmentListParams {
  keyword?: string
  status?: number
  parentId?: number
  page?: number
  pageSize?: number
}

export interface DepartmentCreateRequest {
  name: string
  code: string
  parentId?: number
  leaderId?: number
  contactPhone?: string
  address?: string
  description?: string
  status?: number
}

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  accessToken: string
  refreshToken: string
  tokenType: string
  sessionId: string
  user: UserInfo
}

export interface RefreshTokenRequest {
  refreshToken: string
}

export interface RefreshTokenResponse {
  accessToken: string
  refreshToken?: string
  tokenType: string
}

export interface ChangePasswordRequest {
  oldPassword: string
  newPassword: string
}

export interface ResetPasswordRequest {
  userId: number
  newPassword: string
}

export interface AssignRolesRequest {
  roleIds: number[]
}

export interface SetPrimaryRoleRequest {
  roleId: number
}

export interface AssignPermissionsRequest {
  permissionIds: number[]
}

export interface SortMenusRequest {
  menuIds: number[]
}

export interface PageResponse<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
  pages: number
}

export interface DataPermissionRule {
  id: number
  name: string
  code: string
  permissionId?: number
  resourceTable: string
  ruleType: number
  ruleExpression: string
  description?: string
  status: number
  createTime: string
  updateTime: string
}

export interface DataPermissionRuleListParams {
  keyword?: string
  permissionId?: number
  ruleType?: number
  status?: number
  page?: number
  pageSize?: number
}

export interface DataPermissionRuleCreateRequest {
  name: string
  code: string
  permissionId?: number
  resourceTable: string
  ruleType: number
  ruleExpression: string
  description?: string
  status?: number
}

export interface DataPermissionRuleUpdateRequest {
  name?: string
  code?: string
  permissionId?: number
  resourceTable?: string
  ruleType?: number
  ruleExpression?: string
  description?: string
  status?: number
}

export interface SessionInfo {
  id: number
  userId: number
  sessionId: string
  deviceType?: string
  deviceInfo?: string
  osInfo?: string
  browserInfo?: string
  ipAddress?: string
  loginTime: string
  lastActiveTime: string
  expireTime: string
  status: number
  createTime: string
  updateTime: string
  username?: string
  nickname?: string
}

export interface SessionListParams {
  user_id?: number
  device_type?: string
  status?: number
  keyword?: string
  page?: number
  page_size?: number
}

