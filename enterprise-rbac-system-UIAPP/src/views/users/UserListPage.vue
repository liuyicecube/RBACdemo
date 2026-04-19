<template>
  <div class="user-list-page">
    <div class="page-header">
      <div class="header-left">
        <el-icon class="header-icon" :size="28"><UserFilled /></el-icon>
        <div class="header-title">
          <h1>用户管理</h1>
          <p>管理系统中的用户和角色分配</p>
        </div>
      </div>
      <div class="header-right">
        <el-button :icon="Refresh" @click="loadData" class="icon-btn">
          刷新
        </el-button>
        <el-button type="primary" :icon="Plus" @click="handleCreate" class="primary-btn" v-permission="'user:create'">
          新增用户
        </el-button>
      </div>
    </div>

    <el-card class="main-card" shadow="never">
      <div class="card-content">
        <div class="search-bar">
          <div class="search-items">
            <el-input
              v-model="searchParams.keyword"
              placeholder="搜索用户名/昵称"
              :prefix-icon="Search"
              clearable
              class="search-input"
            />
            <el-select
              v-model="searchParams.status"
              placeholder="状态"
              clearable
              class="search-select"
            >
              <el-option :value="1" label="启用" />
              <el-option :value="0" label="禁用" />
            </el-select>
          </div>
          <div class="search-actions">
            <el-button type="primary" :icon="Search" @click="loadData">搜索</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </div>
        </div>

        <div class="toolbar" v-if="selectedIds.length > 0">
          <div class="selected-info">
            <el-icon><Select /></el-icon>
            <span>已选择 {{ selectedIds.length }} 项</span>
          </div>
          <div class="batch-actions">
            <el-button type="success" :icon="CircleCheck" @click="handleBatchEnable">
              批量启用
            </el-button>
            <el-button type="warning" :icon="CircleClose" @click="handleBatchDisable">
              批量禁用
            </el-button>
            <el-button type="danger" :icon="Delete" @click="handleBatchDelete" v-permission="'user:delete'">
              批量删除
            </el-button>
          </div>
        </div>

        <div class="table-wrapper">
          <el-table
            :data="tableData"
            v-loading="loading"
            stripe
            style="width: 100%"
            @selection-change="handleSelectionChange"
            class="modern-table"
          >
            <el-table-column type="selection" width="55" />
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="username" label="用户名" min-width="120">
              <template #default="{ row }">
                <div class="cell-name">
                  <el-avatar :size="32" :src="row.avatar || ''" style="background: #667eea;">
                    {{ row.username ? row.username.charAt(0).toUpperCase() : 'U' }}
                  </el-avatar>
                  <div class="user-info">
                    <span class="username">{{ row.username }}</span>
                    <span class="nickname">{{ row.nickname }}</span>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="email" label="邮箱" min-width="180" show-overflow-tooltip />
            <el-table-column prop="phone" label="手机号" width="130" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <div class="status-cell">
                  <span class="status-dot" :class="row.status === 1 ? 'active' : 'inactive'"></span>
                  <span>{{ row.status === 1 ? '启用' : '禁用' }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="lastLoginTime" label="最后登录" width="180" />
            <el-table-column label="操作" width="220" fixed="right">
              <template #default="{ row }">
                <div class="action-buttons">
                  <el-button
                    link
                    type="primary"
                    size="small"
                    @click="handleEdit(row)"
                    v-permission="'user:update'"
                  >
                    <el-icon><Edit /></el-icon>
                    编辑
                  </el-button>
                  <el-button
                    link
                    type="primary"
                    size="small"
                    @click="handleAssignRoles(row)"
                    v-permission="'user:update'"
                  >
                    <el-icon><User /></el-icon>
                    角色
                  </el-button>
                  <el-button
                    link
                    type="danger"
                    size="small"
                    @click="handleDelete(row)"
                    v-permission="'user:delete'"
                  >
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <div class="pagination-wrapper">
          <div class="export-btn">
            <el-button :icon="Download" @click="handleExport">
              导出数据
            </el-button>
          </div>
          <el-pagination
            v-model:current-page="pagination.page"
            v-model:page-size="pagination.pageSize"
            :total="pagination.total"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="loadData"
            @current-change="loadData"
          />
        </div>
      </div>
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'create' ? '新增用户' : '编辑用户'"
      width="750px"
      :close-on-click-modal="false"
      class="user-dialog"
    >
      <div class="user-profile-section">
        <div class="profile-header">
          <div class="avatar-section">
            <el-upload
              class="avatar-uploader"
              action="#"
              :show-file-list="false"
              :on-change="handleAvatarChange"
              accept="image/*"
            >
              <el-avatar :size="110" :src="formData.avatar || ''" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                {{ formData.username ? formData.username.charAt(0).toUpperCase() : 'U' }}
              </el-avatar>
              <div class="avatar-overlay">
                <el-icon :size="28"><Camera /></el-icon>
                <span>更换头像</span>
              </div>
            </el-upload>
          </div>
          <div class="user-info-section">
            <h3 class="user-name">{{ formData.nickname || '新用户' }}</h3>
            <p class="user-username">@{{ formData.username || 'username' }}</p>
            <div class="user-meta">
              <el-tag :type="formData.status === 1 ? 'success' : 'danger'" size="small">
                {{ formData.status === 1 ? '启用' : '禁用' }}
              </el-tag>
            </div>
          </div>
        </div>
      </div>

      <el-form ref="formRef" :model="formData" :rules="rules" label-width="100px" class="user-form">
        <el-divider content-position="left">
          <span class="divider-label">
            <el-icon><User /></el-icon>
            基本信息
          </span>
        </el-divider>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="formData.username" :disabled="dialogType === 'edit'" placeholder="请输入用户名" clearable>
                <template #prefix>
                  <el-icon><User /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item v-if="dialogType === 'create'" label="密码" prop="password">
              <el-input v-model="formData.password" type="password" show-password placeholder="请输入密码" clearable @input="checkPasswordStrength">
                <template #prefix>
                  <el-icon><Lock /></el-icon>
                </template>
              </el-input>
              <div class="password-strength" v-if="formData.password">
                <div class="strength-bar">
                  <div class="strength-level" :class="passwordStrengthClass" :style="{ width: passwordStrengthWidth }"></div>
                </div>
                <span class="strength-text">{{ passwordStrengthText }}</span>
              </div>
            </el-form-item>
            <el-form-item v-else label="密码">
              <el-button link type="primary" @click="handleShowResetPassword">
                <el-icon><Key /></el-icon>
                重置密码
              </el-button>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="昵称" prop="nickname">
              <el-input v-model="formData.nickname" placeholder="请输入昵称" clearable>
                <template #prefix>
                  <el-icon><Edit /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-radio-group v-model="formData.status" class="status-radio-group">
                <el-radio :value="1">
                  <span class="radio-content">
                    <el-icon :color="'#10b981'"><CircleCheck /></el-icon>
                    启用
                  </span>
                </el-radio>
                <el-radio :value="0">
                  <span class="radio-content">
                    <el-icon :color="'#ef4444'"><CircleClose /></el-icon>
                    禁用
                  </span>
                </el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="formData.email" placeholder="请输入邮箱" clearable>
                <template #prefix>
                  <el-icon><Message /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="formData.phone" placeholder="请输入手机号" clearable>
                <template #prefix>
                  <el-icon><Phone /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">
          <span class="divider-label">
            <el-icon><OfficeBuilding /></el-icon>
            组织信息
          </span>
        </el-divider>

        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="所属部门" prop="departmentId">
              <el-tree-select
                v-model="formData.departmentId"
                :data="departmentTree"
                :props="{ label: 'name', value: 'id', children: 'children' }"
                placeholder="请选择所属部门"
                clearable
                check-strictly
                filterable
                :filter-node-method="filterDepartment"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">
          <span class="divider-label">
            <el-icon><Setting /></el-icon>
            快速设置
          </span>
        </el-divider>

        <div class="quick-setup">
          <div class="setup-card" @click="applyQuickSetup('admin')">
            <div class="setup-icon" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);">
              <el-icon :size="24"><Trophy /></el-icon>
            </div>
            <div class="setup-info">
              <div class="setup-title">管理员</div>
              <div class="setup-desc">分配全部权限</div>
            </div>
          </div>
          <div class="setup-card" @click="applyQuickSetup('user')">
            <div class="setup-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
              <el-icon :size="24"><UserFilled /></el-icon>
            </div>
            <div class="setup-info">
              <div class="setup-title">普通用户</div>
              <div class="setup-desc">基础查看权限</div>
            </div>
          </div>
          <div class="setup-card" @click="applyQuickSetup('guest')">
            <div class="setup-icon" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
              <el-icon :size="24"><View /></el-icon>
            </div>
            <div class="setup-info">
              <div class="setup-title">访客</div>
              <div class="setup-desc">只读权限</div>
            </div>
          </div>
        </div>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <div class="footer-left">
            <el-tag type="info" size="small">
              <el-icon><InfoFilled /></el-icon>
              {{ dialogType === 'create' ? '创建后用户可以使用账号登录系统' : '修改用户信息将立即生效' }}
            </el-tag>
          </div>
          <div class="footer-right">
            <el-button @click="dialogVisible = false" class="cancel-btn">
              <el-icon><Close /></el-icon>
              取消
            </el-button>
            <el-button type="primary" :loading="submitLoading" @click="handleSubmit" class="submit-btn">
              <el-icon><Check /></el-icon>
              {{ dialogType === 'create' ? '创建用户' : '保存修改' }}
            </el-button>
          </div>
        </div>
      </template>
    </el-dialog>

    <el-dialog
      v-model="showResetPassword"
      title="重置密码"
      width="450px"
      class="reset-password-dialog"
    >
      <el-form ref="resetPasswordFormRef" :model="resetPasswordForm" :rules="resetPasswordRules" label-width="100px">
        <el-form-item label="新密码" prop="newPassword">
          <el-input v-model="resetPasswordForm.newPassword" type="password" show-password placeholder="请输入新密码">
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="resetPasswordForm.confirmPassword" type="password" show-password placeholder="请再次输入新密码">
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showResetPassword = false">取消</el-button>
        <el-button type="primary" :loading="resetPasswordLoading" @click="handleResetPassword">
          <el-icon><Key /></el-icon>
          确认重置
        </el-button>
      </template>
    </el-dialog>

    <el-dialog
      v-model="roleDialogVisible"
      title="分配角色"
      width="900px"
      class="role-dialog"
      :close-on-click-modal="false"
    >
      <div class="role-dialog-header">
        <div class="header-bg"></div>
        <div class="current-user">
          <div class="user-avatar-wrapper">
            <el-avatar :size="64" class="user-avatar">
              {{ currentUserName ? currentUserName.charAt(0).toUpperCase() : 'U' }}
            </el-avatar>
            <div class="avatar-ring"></div>
            <div class="avatar-glow"></div>
          </div>
          <div class="user-info">
            <span class="user-label">为用户分配角色</span>
            <span class="user-name">{{ currentUserName }}</span>
            <div class="user-tag">
              <el-icon><User /></el-icon>
              系统用户
            </div>
          </div>
        </div>
        <div class="role-stats">
          <div class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
              <el-icon><CircleCheck /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-label">已选角色</span>
              <span class="stat-value">{{ checkedRoleCount }}</span>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
              <el-icon><List /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-label">总角色数</span>
              <span class="stat-value">{{ totalRoleCount }}</span>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);">
              <el-icon><View /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-label">可用角色</span>
              <span class="stat-value">{{ activeRoleCount }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="role-toolbar">
        <div class="toolbar-left">
          <div class="filter-tabs">
            <div 
              v-for="tab in filterTabs" 
              :key="tab.key"
              class="filter-tab"
              :class="{ active: activeFilter === tab.key }"
              @click="activeFilter = tab.key"
            >
              <el-icon><component :is="tab.icon" /></el-icon>
              {{ tab.label }}
            </div>
          </div>
        </div>
        <div class="toolbar-center">
          <el-input
            v-model="roleSearch"
            placeholder="搜索角色名称/编码..."
            :prefix-icon="Search"
            clearable
            class="search-input"
          />
        </div>
        <div class="toolbar-right">
          <el-button :icon="List" @click="checkAllRoles" class="action-btn">
            全选
          </el-button>
          <el-button :icon="Delete" @click="uncheckAllRoles" class="action-btn danger">
            清空
          </el-button>
        </div>
      </div>

      <div class="role-grid-wrapper">
        <div class="role-grid">
          <div 
            v-for="role in filteredRoles" 
            :key="role.id" 
            class="role-card"
            :class="{ selected: isRoleSelected(role.id), disabled: !isRoleEnabled(role) }"
            @click="toggleRole(role.id)"
          >
            <div class="role-card-glow"></div>
            <div class="role-card-header">
              <div class="role-icon" :style="getRoleIconStyle(role)">
                <el-icon :size="28"><component :is="getRoleIcon(role)" /></el-icon>
              </div>
              <div class="role-check">
                <el-icon v-if="isRoleSelected(role.id)" :size="24"><CircleCheck /></el-icon>
              </div>
            </div>
            <div class="role-card-body">
              <div class="role-name">{{ role.name }}</div>
              <div class="role-code">{{ role.code }}</div>
              <div class="role-desc" v-if="role.description">{{ role.description }}</div>
            </div>
            <div class="role-card-footer">
              <el-tag size="small" :type="isRoleEnabled(role) ? 'success' : 'danger'">
                {{ isRoleEnabled(role) ? '启用' : '禁用' }}
              </el-tag>
              <el-tag v-if="primaryRoleId === role.id" size="small" type="warning">
                <el-icon><Star /></el-icon>
                主角色
              </el-tag>
              <div class="role-actions" v-if="isRoleSelected(role.id)">
                <el-tooltip :content="primaryRoleId === role.id ? '当前主角色' : '设为主角色'" placement="top">
                  <el-icon 
                    class="action-icon" 
                    :class="{ 'primary': primaryRoleId === role.id }"
                    @click.stop="setPrimaryRole(role.id)"
                  >
                    <Star />
                  </el-icon>
                </el-tooltip>
                <el-tooltip content="查看详情" placement="top">
                  <el-icon class="action-icon" @click.stop="previewRole(role)"><View /></el-icon>
                </el-tooltip>
              </div>
            </div>
          </div>
        </div>
        <div v-if="filteredRoles.length === 0" class="empty-state">
          <div class="empty-icon">
            <el-icon :size="72"><Search /></el-icon>
          </div>
          <p class="empty-text">没有找到匹配的角色</p>
          <p class="empty-hint">试试其他搜索词或切换筛选条件</p>
        </div>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <div class="footer-left">
            <div class="selected-roles-preview" v-if="checkedRoleCount > 0">
              <span class="preview-label">已选择：</span>
              <div class="selected-tags">
                <el-tag 
                  v-for="role in selectedRolesPreview" 
                  :key="role.id"
                  size="small"
                  closable
                  @close="toggleRole(role.id)"
                >
                  {{ role.name }}
                </el-tag>
              </div>
            </div>
            <el-tag v-else type="info">
              <el-icon><InfoFilled /></el-icon>
              请为用户分配相应的角色权限
            </el-tag>
          </div>
          <div class="footer-right">
            <el-button @click="roleDialogVisible = false" class="cancel-btn">
              <el-icon><Close /></el-icon>
              取消
            </el-button>
            <el-button type="primary" :loading="roleSubmitLoading" @click="handleRoleSubmit" class="submit-btn">
              <el-icon><Check /></el-icon>
              保存角色
            </el-button>
          </div>
        </div>
      </template>
    </el-dialog>

    <el-dialog
      v-model="previewDialogVisible"
      title="角色详情"
      width="500px"
      class="preview-dialog"
    >
      <div class="preview-content" v-if="previewingRole">
        <div class="preview-header">
          <div class="preview-icon" :style="getRoleIconStyle(previewingRole)">
            <el-icon :size="40"><component :is="getRoleIcon(previewingRole)" /></el-icon>
          </div>
          <div class="preview-info">
            <h3>{{ previewingRole.name }}</h3>
            <p>{{ previewingRole.code }}</p>
          </div>
        </div>
        <el-divider />
        <div class="preview-details">
          <div class="detail-item">
            <span class="detail-label">状态</span>
            <el-tag :type="isRoleEnabled(previewingRole) ? 'success' : 'danger'">
              {{ isRoleEnabled(previewingRole) ? '启用' : '禁用' }}
            </el-tag>
          </div>
          <div class="detail-item" v-if="previewingRole.description">
            <span class="detail-label">描述</span>
            <span class="detail-value">{{ previewingRole.description }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">角色ID</span>
            <span class="detail-value">{{ previewingRole.id }}</span>
          </div>
        </div>
      </div>
      <template #footer>
        <el-button @click="previewDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules, UploadProps } from 'element-plus'
import { userService, roleService, departmentService } from '@/services'
import type { UserInfo, UserCreateRequest, UserUpdateRequest, RoleSimple, Department } from '@/types'
import { 
  Search, Refresh, Plus, Delete, Download, Edit, User,
  Select, CircleCheck, CircleClose, UserFilled, List, Check,
  Lock, Key, Camera, Message, Phone, OfficeBuilding, InfoFilled, Close,
  Trophy, View, Setting, Star
} from '@element-plus/icons-vue'
import { exportToCSV } from '@/utils/export'
import { formatDate } from '@/utils/date'
import { buildTree } from '@/utils'

const loading = ref(false)
const tableData = ref<UserInfo[]>([])
const allRoles = ref<RoleSimple[]>([])
const allDepartments = ref<Department[]>([])
const selectedRoleIds = ref<number[]>([])
const primaryRoleId = ref<number | null>(null)
const currentUserId = ref<number | null>(null)
const currentUserName = ref('')
const roleSearch = ref('')
const selectedIds = ref<number[]>([])
const activeFilter = ref('all')
const previewDialogVisible = ref(false)
const previewingRole = ref<any>(null)

const searchParams = reactive({
  keyword: '',
  status: undefined as number | undefined
})

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

const dialogVisible = ref(false)
const dialogType = ref<'create' | 'edit'>('create')
const formRef = ref<FormInstance>()
const formData = reactive({
  id: null as number | null,
  username: '',
  password: '',
  nickname: '',
  email: '',
  phone: '',
  avatar: '',
  departmentId: undefined as number | undefined,
  status: 1
})

const resetFormData = () => {
  Object.assign(formData, {
    id: null,
    username: '',
    password: '',
    nickname: '',
    email: '',
    phone: '',
    avatar: '',
    departmentId: undefined,
    status: 1
  })
}

const passwordStrength = ref(0)
const passwordStrengthClass = computed(() => {
  if (passwordStrength.value < 3) return 'weak'
  if (passwordStrength.value < 5) return 'medium'
  return 'strong'
})
const passwordStrengthWidth = computed(() => {
  return `${Math.min(passwordStrength.value * 20, 100)}%`
})
const passwordStrengthText = computed(() => {
  if (passwordStrength.value < 3) return '弱'
  if (passwordStrength.value < 5) return '中等'
  return '强'
})

const rules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 6, max: 20, message: '用户名长度为6-20个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ],
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' },
    { min: 1, max: 50, message: '昵称长度为1-50个字符', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  phone: [
    {
      pattern: /^1[3-9]\d{9}$/,
      message: '请输入正确的手机号格式',
      trigger: 'blur'
    }
  ]
}

const roleDialogVisible = ref(false)
const submitLoading = ref(false)
const roleSubmitLoading = ref(false)

const showResetPassword = ref(false)
const resetPasswordFormRef = ref<FormInstance>()
const resetPasswordLoading = ref(false)
const resetPasswordForm = reactive({
  newPassword: '',
  confirmPassword: ''
})

const resetPasswordRules: FormRules = {
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    {
      validator: (_rule, value, callback) => {
        if (value !== resetPasswordForm.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const departmentTree = computed(() => {
  return buildTree(allDepartments.value)
})

const filterDepartment = (value: string, data: any) => {
  if (!value) return true
  return data.name.toLowerCase().includes(value.toLowerCase())
}

const loadData = async () => {
  loading.value = true
  try {
    const data = await userService.getUsers({
      ...searchParams,
      page: pagination.page,
      pageSize: pagination.pageSize
    })
    tableData.value = data.items
    pagination.total = data.total
  } finally {
    loading.value = false
  }
}

const loadAllDepartments = async () => {
  const departments = await departmentService.getAllDepartments()
  allDepartments.value = departments
}

const resetSearch = () => {
  searchParams.keyword = ''
  searchParams.status = undefined
  pagination.page = 1
  loadData()
}

const handleCreate = async () => {
  await loadAllDepartments()
  dialogType.value = 'create'
  resetFormData()
  passwordStrength.value = 0
  dialogVisible.value = true
}

const handleEdit = async (row: UserInfo) => {
  await loadAllDepartments()
  dialogType.value = 'edit'
  Object.assign(formData, {
    id: row.id,
    username: row.username,
    password: '',
    nickname: row.nickname,
    email: row.email || '',
    phone: row.phone || '',
    avatar: row.avatar || '',
    departmentId: row.departmentId !== undefined ? row.departmentId : (row as any).department_id,
    status: row.status !== undefined ? row.status : (row as any).status
  })
  passwordStrength.value = 0
  dialogVisible.value = true
}

const checkPasswordStrength = () => {
  const password = formData.password
  let strength = 0
  
  if (password.length >= 6) strength++
  if (password.length >= 8) strength++
  if (/[a-z]/.test(password)) strength++
  if (/[A-Z]/.test(password)) strength++
  if (/[0-9]/.test(password)) strength++
  if (/[^a-zA-Z0-9]/.test(password)) strength++
  
  passwordStrength.value = strength
}

const applyQuickSetup = (type: string) => {
  switch (type) {
    case 'admin':
      formData.status = 1
      ElMessage.info('已应用管理员配置 - 请手动分配角色')
      break
    case 'user':
      formData.status = 1
      ElMessage.info('已应用普通用户配置 - 请手动分配角色')
      break
    case 'guest':
      formData.status = 1
      ElMessage.info('已应用访客配置 - 请手动分配角色')
      break
  }
}

const handleShowResetPassword = () => {
  resetPasswordForm.newPassword = ''
  resetPasswordForm.confirmPassword = ''
  showResetPassword.value = true
}

const handleAvatarChange: UploadProps['onChange'] = (uploadFile) => {
  const raw = uploadFile.raw as File
  if (raw) {
    const reader = new FileReader()
    reader.onload = (e) => {
      formData.avatar = e.target?.result as string
    }
    reader.readAsDataURL(raw)
  }
}

const handleResetPassword = async () => {
  if (!resetPasswordFormRef.value || !formData.id) return
  await resetPasswordFormRef.value.validate(async (valid) => {
    if (valid) {
      resetPasswordLoading.value = true
      try {
        await userService.resetPassword({
          userId: formData.id as number,
          newPassword: resetPasswordForm.newPassword
        })
        ElMessage.success('密码重置成功')
        showResetPassword.value = false
        resetPasswordForm.newPassword = ''
        resetPasswordForm.confirmPassword = ''
      } finally {
        resetPasswordLoading.value = false
      }
    }
  })
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitLoading.value = true
      try {
        if (dialogType.value === 'create') {
          const createData: UserCreateRequest = {
            username: formData.username,
            password: formData.password,
            nickname: formData.nickname,
            email: formData.email || undefined,
            phone: formData.phone || undefined,
            avatar: formData.avatar || undefined,
            departmentId: formData.departmentId,
            status: formData.status
          }
          await userService.createUser(createData)
          ElMessage.success('创建成功')
        } else {
          const updateData: UserUpdateRequest = {
            nickname: formData.nickname,
            email: formData.email || undefined,
            phone: formData.phone || undefined,
            avatar: formData.avatar || undefined,
            departmentId: formData.departmentId,
            status: formData.status
          }
          if (formData.password) {
            updateData.password = formData.password
          }
          await userService.updateUser(formData.id!, updateData)
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        loadData()
      } finally {
        submitLoading.value = false
      }
    }
  })
}

const handleDelete = async (row: UserInfo) => {
  try {
    await ElMessageBox.confirm('确定要删除该用户吗?', '提示', {
      type: 'warning'
    })
    await userService.deleteUser(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch {
  }
}

const handleAssignRoles = async (row: UserInfo) => {
  currentUserId.value = row.id
  currentUserName.value = row.username
  roleSearch.value = ''
  await loadAllRoles()
  const userRoles = await userService.getUserRoles(row.id)
  selectedRoleIds.value = userRoles.roles.map((r) => r.id)
  const primaryRole = userRoles.roles.find((r) => r.isPrimary)
  primaryRoleId.value = primaryRole ? primaryRole.id : null
  roleDialogVisible.value = true
}

const loadAllRoles = async () => {
  const rawRoles = await roleService.getAllRoles()
  
  // 直接使用，不再做额外处理
  allRoles.value = rawRoles
}

const totalRoleCount = computed(() => {
  return allRoles.value.length
})

const checkedRoleCount = computed(() => {
  return selectedRoleIds.value.length
})

const filterTabs = [
  { key: 'all', label: '全部', icon: List },
  { key: 'selected', label: '已选', icon: CircleCheck },
  { key: 'available', label: '可用', icon: View },
  { key: 'starred', label: '常用', icon: Star }
]

const selectedRolesPreview = computed(() => {
  return allRoles.value.filter(role => selectedRoleIds.value.includes(role.id))
})

const activeRoleCount = computed(() => {
  return allRoles.value.filter(role => isRoleEnabled(role)).length
})

const filteredRoles = computed(() => {
  let roles = allRoles.value
  
  if (activeFilter.value === 'selected') {
    roles = roles.filter(role => selectedRoleIds.value.includes(role.id))
  } else if (activeFilter.value === 'available') {
    roles = roles.filter(role => isRoleEnabled(role) && !selectedRoleIds.value.includes(role.id))
  } else if (activeFilter.value === 'starred') {
    roles = roles.filter(role => role.id === 1 || role.id === 2)
  }
  
  if (roleSearch.value) {
    roles = roles.filter(role => 
      role.name.toLowerCase().includes(roleSearch.value.toLowerCase()) ||
      role.code?.toLowerCase().includes(roleSearch.value.toLowerCase())
    )
  }
  
  return roles
})

const previewRole = (role: any) => {
  previewingRole.value = role
  previewDialogVisible.value = true
}

const isRoleSelected = (roleId: number) => {
  return selectedRoleIds.value.includes(roleId)
}

const isRoleEnabled = (role: any) => {
  // 简单直接：只要不是 0, false, '0', 'false' 就是启用
  return role.status !== 0 && role.status !== false && role.status !== '0' && role.status !== 'false'
}

const toggleRole = (roleId: number) => {
  const role = allRoles.value.find(r => r.id === roleId)
  
  if (!role) return
  
  if (!isRoleEnabled(role)) {
    ElMessage.warning('该角色已禁用，无法选择')
    return
  }
  
  const index = selectedRoleIds.value.indexOf(roleId)
  if (index > -1) {
    selectedRoleIds.value.splice(index, 1)
    if (primaryRoleId.value === roleId) {
      primaryRoleId.value = null
    }
  } else {
    selectedRoleIds.value.push(roleId)
    if (selectedRoleIds.value.length === 1) {
      primaryRoleId.value = roleId
    }
  }
}

const getRoleIcon = (role: any) => {
  return (role as any).icon || 'Key'
}

const getRoleIconStyle = (role: any) => {
  const color = (role as any).color || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  return { background: color }
}

const checkAllRoles = () => {
  selectedRoleIds.value = allRoles.value.map(role => role.id)
}

const uncheckAllRoles = () => {
  selectedRoleIds.value = []
}

const setPrimaryRole = async (roleId: number) => {
  if (!currentUserId.value) return
  
  const role = allRoles.value.find(r => r.id === roleId)
  
  if (!role) return
  
  if (!isRoleEnabled(role)) {
    ElMessage.warning('该角色已禁用，无法设为主角色')
    return
  }
  
  try {
    await userService.setPrimaryRole(currentUserId.value, { roleId })
    primaryRoleId.value = roleId
    ElMessage.success('设置主角色成功')
  } catch (error) {
    ElMessage.error('设置主角色失败')
  }
}

const handleRoleSubmit = async () => {
  if (!currentUserId.value) return
  roleSubmitLoading.value = true
  try {
    await userService.assignRoles(currentUserId.value, { roleIds: selectedRoleIds.value })
    
    if (selectedRoleIds.value.length > 0 && primaryRoleId.value) {
      if (selectedRoleIds.value.includes(primaryRoleId.value)) {
        await userService.setPrimaryRole(currentUserId.value, { roleId: primaryRoleId.value })
      } else {
        await userService.setPrimaryRole(currentUserId.value, { roleId: selectedRoleIds.value[0] })
      }
    }
    
    ElMessage.success('分配成功')
    roleDialogVisible.value = false
    loadData()
  } finally {
    roleSubmitLoading.value = false
  }
}

const handleSelectionChange = (selection: UserInfo[]) => {
  selectedIds.value = selection.map(item => item.id)
}

const handleBatchEnable = async () => {
  try {
    await ElMessageBox.confirm(`确定要启用选中的 ${selectedIds.value.length} 个用户吗?`, '提示', {
      type: 'success'
    })
    const promises = selectedIds.value.map(id => userService.updateUser(id, { status: 1 }))
    await Promise.all(promises)
    ElMessage.success('批量启用成功')
    selectedIds.value = []
    loadData()
  } catch {
  }
}

const handleBatchDisable = async () => {
  try {
    await ElMessageBox.confirm(`确定要禁用选中的 ${selectedIds.value.length} 个用户吗?`, '提示', {
      type: 'warning'
    })
    const promises = selectedIds.value.map(id => userService.updateUser(id, { status: 0 }))
    await Promise.all(promises)
    ElMessage.success('批量禁用成功')
    selectedIds.value = []
    loadData()
  } catch {
  }
}

const handleBatchDelete = async () => {
  try {
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedIds.value.length} 个用户吗?`, '提示', {
      type: 'warning'
    })
    const promises = selectedIds.value.map(id => userService.deleteUser(id))
    await Promise.all(promises)
    ElMessage.success('批量删除成功')
    selectedIds.value = []
    loadData()
  } catch {
  }
}

const handleExport = () => {
  const headers = [
    { key: 'id', title: 'ID' },
    { key: 'username', title: '用户名' },
    { key: 'nickname', title: '昵称' },
    { key: 'email', title: '邮箱' },
    { key: 'phone', title: '手机号' },
    { key: 'status', title: '状态' },
    { key: 'lastLoginTime', title: '最后登录时间' }
  ]
  
  const exportData = tableData.value.map(item => ({
    ...item,
    status: item.status === 1 ? '启用' : '禁用'
  }))
  
  const filename = `用户数据_${formatDate(new Date(), 'YYYY-MM-DD')}`
  exportToCSV(exportData, filename, headers)
  ElMessage.success('导出成功')
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';

.user-list-page {
  padding: 24px;
  background: $background-page;
  min-height: calc(100vh - 60px);

  .user-dialog {
    :deep(.el-dialog__header) {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 20px 24px;
      
      .el-dialog__title {
        color: #fff;
        font-weight: 700;
        font-size: 18px;
        display: flex;
        align-items: center;
        gap: 10px;
      }
      
      .el-dialog__headerbtn {
        .el-dialog__close {
          color: #fff;
          font-size: 20px;
          
          &:hover {
            color: rgba(255, 255, 255, 0.8);
          }
        }
      }
    }

    :deep(.el-dialog__body) {
      padding: 24px;
    }

    .user-profile-section {
      margin-bottom: 24px;
      padding: 28px;
      background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
      border-radius: $border-radius-xl;

      .profile-header {
        display: flex;
        align-items: center;
        gap: 28px;

        .avatar-section {
          position: relative;

          .avatar-uploader {
            position: relative;
            cursor: pointer;

            .avatar-overlay {
              position: absolute;
              top: 0;
              left: 0;
              width: 110px;
              height: 110px;
              border-radius: 50%;
              background: rgba(0, 0, 0, 0.6);
              display: flex;
              flex-direction: column;
              align-items: center;
              justify-content: center;
              color: #fff;
              opacity: 0;
              transition: opacity 0.3s;

              span {
                font-size: 12px;
                margin-top: 6px;
              }
            }

            &:hover .avatar-overlay {
              opacity: 1;
            }
          }
        }

        .user-info-section {
          flex: 1;

          .user-name {
            font-size: 28px;
            font-weight: 700;
            color: $text-primary;
            margin: 0 0 6px 0;
          }

          .user-username {
            font-size: 15px;
            color: $text-secondary;
            margin: 0 0 14px 0;
          }

          .user-meta {
            display: flex;
            gap: 8px;
          }
        }
      }
    }

    .password-strength {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-top: 8px;

      .strength-bar {
        flex: 1;
        height: 6px;
        background: #e2e8f0;
        border-radius: 3px;
        overflow: hidden;

        .strength-level {
          height: 100%;
          border-radius: 3px;
          transition: all 0.3s;

          &.weak {
            background: linear-gradient(90deg, #ef4444 0%, #f87171 100%);
          }

          &.medium {
            background: linear-gradient(90deg, #f59e0b 0%, #fbbf24 100%);
          }

          &.strong {
            background: linear-gradient(90deg, #10b981 0%, #34d399 100%);
          }
        }
      }

      .strength-text {
        font-size: 12px;
        font-weight: 500;
        min-width: 40px;
        text-align: right;

        &:has(+ .weak) {
          color: #ef4444;
        }

        &:has(+ .medium) {
          color: #f59e0b;
        }

        &:has(+ .strong) {
          color: #10b981;
        }
      }
    }

    .status-radio-group {
      display: flex;
      gap: 16px;

      .radio-content {
        display: flex;
        align-items: center;
        gap: 6px;
      }
    }

    .quick-setup {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin-top: 8px;

      .setup-card {
        padding: 16px;
        background: #fff;
        border: 2px solid $border-lighter;
        border-radius: $border-radius-lg;
        cursor: pointer;
        transition: all 0.3s;
        display: flex;
        align-items: center;
        gap: 12px;

        &:hover {
          border-color: $primary-color;
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
        }

        .setup-icon {
          width: 48px;
          height: 48px;
          border-radius: $border-radius-lg;
          display: flex;
          align-items: center;
          justify-content: center;
          color: #fff;
          flex-shrink: 0;
        }

        .setup-info {
          flex: 1;

          .setup-title {
            font-size: 15px;
            font-weight: 600;
            color: $text-primary;
            margin-bottom: 2px;
          }

          .setup-desc {
            font-size: 12px;
            color: $text-secondary;
          }
        }
      }
    }

    .user-form {
      .divider-label {
        display: flex;
        align-items: center;
        gap: 6px;
        font-weight: 600;
        color: $text-regular;
      }

      :deep(.el-form-item__label) {
        font-weight: 500;
        color: $text-regular;
      }
    }

    :deep(.el-dialog__footer) {
      padding: 16px 24px;
      background: #f8fafc;
      border-top: 1px solid $border-lighter;

      .dialog-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;

        .footer-left {
          .el-tag {
            border-radius: $border-radius-md;
          }
        }

        .footer-right {
          display: flex;
          gap: 12px;

          .el-button {
            border-radius: $border-radius-md;
            font-weight: 500;
            padding: 10px 24px;
            transition: all 0.3s;

            &:hover {
              transform: translateY(-1px);
            }

            &.cancel-btn {
              border-color: $border-color;
              color: $text-regular;

              &:hover {
                border-color: $primary-color;
                color: $primary-color;
              }
            }

            &.submit-btn {
              background: $gradient-primary;
              border: none;
              box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            }
          }
        }
      }
    }
  }

  .reset-password-dialog {
    :deep(.el-dialog__header) {
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      padding: 20px 24px;
      
      .el-dialog__title {
        color: #fff;
        font-weight: 700;
        font-size: 18px;
        display: flex;
        align-items: center;
        gap: 10px;
      }
      
      .el-dialog__headerbtn {
        .el-dialog__close {
          color: #fff;
          font-size: 20px;
          
          &:hover {
            color: rgba(255, 255, 255, 0.8);
          }
        }
      }
    }
  }

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;

    .header-left {
      display: flex;
      align-items: center;
      gap: 16px;

      .header-icon {
        color: $primary-color;
      }

      .header-title {
        h1 {
          font-size: 24px;
          font-weight: 700;
          color: $text-primary;
          margin: 0 0 4px 0;
        }

        p {
          font-size: 14px;
          color: $text-secondary;
          margin: 0;
        }
      }
    }

    .header-right {
      display: flex;
      gap: 12px;

      .icon-btn {
        border-radius: $border-radius-lg;
      }

      .primary-btn {
        border-radius: $border-radius-lg;
        padding: 10px 20px;
      }
    }
  }

  .main-card {
    border-radius: $border-radius-xl;
    border: none;

    .card-content {
      padding: 24px;
    }

    .search-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      padding: 20px;
      background: $background-color;
      border-radius: $border-radius-lg;

      .search-items {
        display: flex;
        gap: 12px;

        .search-input {
          width: 280px;
        }

        .search-select {
          width: 140px;
        }
      }

      .search-actions {
        display: flex;
        gap: 12px;
      }
    }

    .toolbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      padding: 16px 20px;
      background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
      border-radius: $border-radius-lg;
      border: 1px solid $border-lighter;

      .selected-info {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 14px;
        color: $text-regular;
      }

      .batch-actions {
        display: flex;
        gap: 12px;
      }
    }

    .table-wrapper {
      .modern-table {
        border-radius: $border-radius;
        overflow: hidden;

        :deep(.el-table__header-wrapper) {
          th {
            background: $background-color;
            color: $text-regular;
            font-weight: 600;
          }
        }

        .cell-name {
          display: flex;
          align-items: center;
          gap: 12px;

          .user-info {
            display: flex;
            flex-direction: column;
            gap: 2px;

            .username {
              font-weight: 500;
              color: $text-primary;
              font-size: 14px;
            }

            .nickname {
              font-size: 12px;
              color: $text-secondary;
            }
          }
        }

        .status-cell {
          display: flex;
          align-items: center;
          gap: 6px;

          .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;

            &.active {
              background: $success-color;
            }

            &.inactive {
              background: $danger-color;
            }
          }
        }

        .action-buttons {
          display: flex;
          gap: 4px;
        }
      }
    }

    .pagination-wrapper {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 24px;
      padding-top: 20px;
      border-top: 1px solid $border-lighter;
    }
  }

  .role-dialog {
    :deep(.el-dialog__header) {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 20px 24px;
      
      .el-dialog__title {
        color: #fff;
        font-weight: 700;
        font-size: 18px;
        display: flex;
        align-items: center;
        gap: 10px;
      }
      
      .el-dialog__headerbtn {
        .el-dialog__close {
          color: #fff;
          font-size: 20px;
          
          &:hover {
            color: rgba(255, 255, 255, 0.8);
          }
        }
      }
    }

    :deep(.el-dialog__body) {
      padding: 0;
    }

    .role-dialog-header {
      padding: 32px 24px;
      background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
      border-bottom: 1px solid $border-lighter;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: relative;
      overflow: hidden;

      .header-bg {
        position: absolute;
        top: -50%;
        right: -20%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
        border-radius: 50%;
        animation: float 6s ease-in-out infinite;
      }

      .current-user {
        display: flex;
        align-items: center;
        gap: 20px;
        position: relative;
        z-index: 1;

        .user-avatar-wrapper {
          position: relative;

          .user-avatar {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
            z-index: 2;
            position: relative;
          }

          .avatar-ring {
            position: absolute;
            top: -6px;
            left: -6px;
            right: -6px;
            bottom: -6px;
            border: 3px solid rgba(102, 126, 234, 0.4);
            border-radius: 50%;
            animation: pulse-ring 2s ease-out infinite;
          }

          .avatar-glow {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 80px;
            height: 80px;
            background: radial-gradient(circle, rgba(102, 126, 234, 0.3) 0%, transparent 70%);
            border-radius: 50%;
            animation: glow-pulse 3s ease-in-out infinite;
          }
        }

        .user-info {
          display: flex;
          flex-direction: column;

          .user-label {
            font-size: 13px;
            color: $text-secondary;
            margin-bottom: 4px;
            font-weight: 500;
          }

          .user-name {
            font-size: 22px;
            font-weight: 700;
            color: $text-primary;
            margin-bottom: 8px;
          }

          .user-tag {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 4px 12px;
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            border-radius: 20px;
            font-size: 12px;
            color: $primary-color;
            font-weight: 500;
          }
        }
      }

      .role-stats {
        display: flex;
        gap: 16px;
        position: relative;
        z-index: 1;

        .stat-card {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 14px 18px;
          background: #fff;
          border-radius: $border-radius-xl;
          box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
          transition: all 0.3s;

          &:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
          }

          .stat-icon {
            width: 44px;
            height: 44px;
            border-radius: $border-radius-lg;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
          }

          .stat-content {
            display: flex;
            flex-direction: column;

            .stat-label {
              font-size: 12px;
              color: $text-secondary;
              margin-bottom: 2px;
            }

            .stat-value {
              font-size: 24px;
              font-weight: 700;
              color: $text-primary;
              line-height: 1;
            }
          }
        }
      }
    }

    .role-toolbar {
      padding: 20px 24px;
      background: #fff;
      border-bottom: 1px solid $border-lighter;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;

      .toolbar-left {
        .filter-tabs {
          display: flex;
          gap: 4px;
          padding: 4px;
          background: $background-color;
          border-radius: $border-radius-lg;

          .filter-tab {
            padding: 8px 16px;
            border-radius: $border-radius-md;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 13px;
            font-weight: 500;
            color: $text-secondary;

            &:hover {
              color: $primary-color;
              background: rgba(102, 126, 234, 0.05);
            }

            &.active {
              background: #fff;
              color: $primary-color;
              box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            }
          }
        }
      }

      .toolbar-center {
        flex: 1;
        max-width: 400px;

        .search-input {
          width: 100%;

          :deep(.el-input__wrapper) {
            border-radius: $border-radius-lg;
            box-shadow: 0 0 0 1px $border-color inset;
            transition: all 0.3s;

            &:hover {
              box-shadow: 0 0 0 1px $primary-color inset;
            }

            &.is-focus {
              box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) inset;
            }
          }
        }
      }

      .toolbar-right {
        display: flex;
        gap: 8px;

        .action-btn {
          border-radius: $border-radius-md;
          font-weight: 500;
          transition: all 0.3s;
          display: flex;
          align-items: center;
          gap: 6px;

          &:hover {
            transform: translateY(-1px);
          }

          &.danger {
            &:hover {
              background: #fee2e2;
              color: #ef4444;
              border-color: #ef4444;
            }
          }
        }
      }
    }

    .role-grid-wrapper {
      padding: 24px;
      max-height: 420px;
      overflow-y: auto;

      .role-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
        gap: 18px;
      }

      .role-card {
        position: relative;
        padding: 20px;
        background: #fff;
        border: 2px solid $border-lighter;
        border-radius: $border-radius-xl;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        overflow: hidden;

        &.disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        &:not(.disabled):hover {
          border-color: $primary-color;
          transform: translateY(-4px) scale(1.02);
          box-shadow: 0 12px 32px rgba(102, 126, 234, 0.25);

          .role-card-glow {
            opacity: 1;
          }
        }

        &.selected {
          border-color: $primary-color;
          background: linear-gradient(135deg, #667eea10 0%, #764ba210 100%);
          box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2);

          .role-card-glow {
            opacity: 1;
            animation: selected-glow 2s ease-in-out infinite;
          }
        }

        .role-card-glow {
          position: absolute;
          top: -50%;
          left: -50%;
          width: 200%;
          height: 200%;
          background: radial-gradient(circle, rgba(102, 126, 234, 0.15) 0%, transparent 60%);
          opacity: 0;
          transition: opacity 0.4s;
          pointer-events: none;
        }

        .role-card-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 14px;
          position: relative;
          z-index: 1;

          .role-icon {
            width: 56px;
            height: 56px;
            border-radius: $border-radius-xl;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
            transition: all 0.4s;
          }

          .role-check {
            width: 28px;
            height: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: $primary-color;

            .el-icon {
              animation: check-pop 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            }
          }
        }

        .role-card-body {
          margin-bottom: 14px;
          position: relative;
          z-index: 1;

          .role-name {
            font-size: 16px;
            font-weight: 700;
            color: $text-primary;
            margin-bottom: 4px;
          }

          .role-code {
            font-size: 13px;
            color: $text-secondary;
            margin-bottom: 6px;
          }

          .role-desc {
            font-size: 12px;
            color: $text-secondary;
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
          }
        }

        .role-card-footer {
          display: flex;
          align-items: center;
          justify-content: space-between;
          position: relative;
          z-index: 1;

          .role-actions {
            display: flex;
            gap: 8px;

            .action-icon {
              width: 28px;
              height: 28px;
              display: flex;
              align-items: center;
              justify-content: center;
              border-radius: 50%;
              background: rgba(102, 126, 234, 0.1);
              color: $primary-color;
              transition: all 0.3s;
              cursor: pointer;

              &:hover {
                background: $primary-color;
                color: #fff;
                transform: scale(1.1);
              }

              &.primary {
                background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                color: #fff;
                box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);

                &:hover {
                  transform: scale(1.1);
                  box-shadow: 0 6px 16px rgba(245, 158, 11, 0.5);
                }
              }
            }
          }
        }
      }

      .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 60px 24px;
        color: $text-secondary;

        .empty-icon {
          width: 120px;
          height: 120px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
          border-radius: 50%;
          margin-bottom: 20px;

          .el-icon {
            color: $border-color;
          }
        }

        .empty-text {
          margin: 0 0 8px 0;
          font-size: 16px;
          font-weight: 600;
          color: $text-regular;
        }

        .empty-hint {
          margin: 0;
          font-size: 14px;
          color: $text-secondary;
        }
      }
    }

    :deep(.el-dialog__footer) {
      padding: 16px 24px;
      background: #f8fafc;
      border-top: 1px solid $border-lighter;

      .dialog-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;

        .footer-left {
          flex: 1;
          min-width: 0;

          .selected-roles-preview {
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;

            .preview-label {
              font-size: 13px;
              color: $text-regular;
              font-weight: 500;
              flex-shrink: 0;
            }

            .selected-tags {
              display: flex;
              gap: 6px;
              flex-wrap: wrap;
              flex: 1;
              min-width: 0;

              .el-tag {
                border-radius: $border-radius-md;
              }
            }
          }

          .el-tag {
            border-radius: $border-radius-md;
            display: flex;
            align-items: center;
            gap: 4px;
          }
        }

        .footer-right {
          display: flex;
          gap: 12px;
          flex-shrink: 0;

          .el-button {
            border-radius: $border-radius-md;
            font-weight: 500;
            padding: 10px 24px;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 6px;

            &:hover {
              transform: translateY(-1px);
            }

            &.cancel-btn {
              border-color: $border-color;
              color: $text-regular;

              &:hover {
                border-color: $primary-color;
                color: $primary-color;
              }
            }

            &.submit-btn {
              background: $gradient-primary;
              border: none;
              box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            }
          }
        }
      }
    }
  }

  @keyframes pulse-ring {
    0% {
      transform: scale(1);
      opacity: 1;
    }
    100% {
      transform: scale(1.2);
      opacity: 0;
    }
  }

  @keyframes check-pop {
    0% {
      transform: scale(0);
    }
    50% {
      transform: scale(1.2);
    }
    100% {
      transform: scale(1);
    }
  }

  @keyframes glow-pulse {
    0%, 100% {
      opacity: 0.5;
      transform: translate(-50%, -50%) scale(1);
    }
    50% {
      opacity: 1;
      transform: translate(-50%, -50%) scale(1.1);
    }
  }

  @keyframes float {
    0%, 100% {
      transform: translateY(0);
    }
    50% {
      transform: translateY(-20px);
    }
  }

  @keyframes selected-glow {
    0%, 100% {
      opacity: 0.8;
    }
    50% {
      opacity: 1;
    }
  }
}

.preview-dialog {
  :deep(.el-dialog__header) {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px 24px;
    
    .el-dialog__title {
      color: #fff;
      font-weight: 700;
      font-size: 18px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    
    .el-dialog__headerbtn {
      .el-dialog__close {
        color: #fff;
        font-size: 20px;
        
        &:hover {
          color: rgba(255, 255, 255, 0.8);
        }
      }
    }
  }

  :deep(.el-dialog__body) {
    padding: 24px;
  }

  .preview-content {
    .preview-header {
      display: flex;
      align-items: center;
      gap: 20px;
      padding: 20px;
      background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
      border-radius: $border-radius-xl;

      .preview-icon {
        width: 72px;
        height: 72px;
        border-radius: $border-radius-xl;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #fff;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
      }

      .preview-info {
        flex: 1;

        h3 {
          margin: 0 0 6px 0;
          font-size: 22px;
          font-weight: 700;
          color: $text-primary;
        }

        p {
          margin: 0;
          font-size: 14px;
          color: $text-secondary;
        }
      }
    }

    .preview-details {
      margin-top: 20px;

      .detail-item {
        display: flex;
        padding: 14px 0;
        border-bottom: 1px solid $border-lighter;

        &:last-child {
          border-bottom: none;
        }

        .detail-label {
          width: 100px;
          font-weight: 500;
          color: $text-secondary;
          flex-shrink: 0;
        }

        .detail-value {
          flex: 1;
          color: $text-primary;
        }
      }
    }
  }
}
</style>
