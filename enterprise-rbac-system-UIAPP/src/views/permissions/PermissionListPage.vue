<template>
  <div class="permission-list-page">
    <div class="page-header">
      <div class="header-left">
        <el-icon class="header-icon" :size="28"><Key /></el-icon>
        <div class="header-title">
          <h1>权限管理</h1>
          <p>管理系统中的权限和资源配置</p>
        </div>
      </div>
      <div class="header-right">
        <el-button :icon="Refresh" @click="loadData" class="icon-btn">
          刷新
        </el-button>
        <el-button type="primary" :icon="Plus" @click="handleCreate" class="primary-btn" v-permission="'permission:create'">
          新增权限
        </el-button>
      </div>
    </div>

    <el-card class="main-card" shadow="never">
      <div class="card-content">
        <div class="search-bar">
          <div class="search-items">
            <el-input
              v-model="searchParams.keyword"
              placeholder="搜索权限名称/编码"
              :prefix-icon="Search"
              clearable
              class="search-input"
            />
            <el-select
              v-model="searchParams.type"
              placeholder="类型"
              clearable
              class="search-select"
            >
              <el-option :value="0" label="菜单" />
              <el-option :value="1" label="按钮" />
              <el-option :value="2" label="API" />
              <el-option :value="3" label="数据" />
              <el-option :value="4" label="字段" />
            </el-select>
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
            <el-button type="danger" :icon="Delete" @click="handleBatchDelete" v-permission="'permission:delete'">
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
            <el-table-column prop="name" label="权限名称" min-width="220">
              <template #default="{ row }">
                <div class="cell-name">
                  <div class="permission-icon-mini" :style="{ background: (row as any).color || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }">
                    <el-icon><component :is="(row as any).icon || 'Key'" /></el-icon>
                  </div>
                  <div class="permission-info-mini">
                    <div class="permission-name-mini">{{ row.name }}</div>
                    <el-tag size="small" type="info">{{ row.code }}</el-tag>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
            <el-table-column label="权限类型" width="120">
              <template #default="{ row }">
                <el-tag :type="getPermissionTypeTagType(row.type)">
                  {{ getPermissionTypeLabel(row.type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <div class="status-cell">
                  <span class="status-dot" :class="row.status === 1 ? 'active' : 'inactive'"></span>
                  <span>{{ row.status === 1 ? '启用' : '禁用' }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="{ row }">
                <div class="action-buttons">
                  <el-button
                    link
                    type="primary"
                    size="small"
                    @click="handleEdit(row)"
                    v-permission="'permission:update'"
                  >
                    <el-icon><Edit /></el-icon>
                    编辑
                  </el-button>
                  <el-button
                    link
                    type="primary"
                    size="small"
                    @click="handleViewRoles(row)"
                  >
                    <el-icon><UserFilled /></el-icon>
                    角色
                  </el-button>
                  <el-button
                    link
                    type="danger"
                    size="small"
                    @click="handleDelete(row)"
                    v-permission="'permission:delete'"
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
      :title="dialogType === 'create' ? '新增权限' : '编辑权限'"
      width="750px"
      :close-on-click-modal="false"
      class="permission-dialog"
    >
      <div class="permission-profile-section">
        <div class="profile-header">
          <div class="permission-icon-section">
            <div class="permission-icon-display" :style="{ background: formData.color || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }">
              <el-icon :size="44"><component :is="formData.icon || 'Key'" /></el-icon>
            </div>
          </div>
          <div class="permission-info-section">
            <div class="permission-name-display">{{ formData.name || '权限名称' }}</div>
            <div class="permission-code-display">{{ formData.code || 'PERMISSION_CODE' }}</div>
            <div class="permission-status">
              <el-tag size="small" :type="formData.status === 1 ? 'success' : 'danger'">
                {{ formData.status === 1 ? '启用' : '禁用' }}
              </el-tag>
            </div>
          </div>
        </div>
      </div>

      <el-form ref="formRef" :model="formData" :rules="rules" label-width="100px" class="permission-form">
        <el-divider content-position="left">
          <span class="divider-title">
            <el-icon><Setting /></el-icon>
            基本信息
          </span>
        </el-divider>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="权限名称" prop="name">
              <el-input v-model="formData.name" placeholder="请输入权限名称" clearable>
                <template #prefix>
                  <el-icon><Document /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="权限编码" prop="code">
              <el-input v-model="formData.code" placeholder="请输入权限编码" :disabled="dialogType === 'edit'" clearable>
                <template #prefix>
                  <el-icon><Key /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="权限类型" prop="type">
              <el-select v-model="formData.type" placeholder="选择权限类型" style="width: 100%">
                <el-option :value="0" label="菜单" />
                <el-option :value="1" label="按钮" />
                <el-option :value="2" label="API" />
                <el-option :value="3" label="数据" />
                <el-option :value="4" label="字段" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="资源类型" prop="resourceType">
              <el-input v-model="formData.resourceType" placeholder="如: user" clearable>
                <template #prefix>
                  <el-icon><Box /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="父权限">
              <el-tree-select
                v-model="formData.parentId"
                :data="permissionTree"
                :props="{ label: 'name', value: 'id', children: 'children' }"
                placeholder="选择父权限"
                clearable
                check-strictly
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="权限颜色">
              <div class="color-picker-wrapper">
                <el-color-picker 
                  v-model="formData.color" 
                  show-alpha
                  :predefine="predefinedColors"
                  popper-class="permission-color-picker"
                />
                <div class="color-preview" :style="{ background: formData.color || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }"></div>
              </div>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="权限图标">
              <el-select v-model="formData.icon" placeholder="选择权限图标" clearable style="width: 100%">
                <el-option 
                  v-for="icon in availableIcons" 
                  :key="icon"
                  :label="icon" 
                  :value="icon"
                >
                  <div class="icon-option">
                    <el-icon><component :is="icon" /></el-icon>
                    <span>{{ icon }}</span>
                  </div>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
          </el-col>
        </el-row>

        <el-divider content-position="left">
          <span class="divider-title">
            <el-icon><Document /></el-icon>
            详细信息
          </span>
        </el-divider>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="操作" prop="action">
              <el-select v-model="formData.action" placeholder="选择操作" clearable style="width: 100%">
                <el-option label="查看" value="view" />
                <el-option label="新增" value="create" />
                <el-option label="编辑" value="update" />
                <el-option label="删除" value="delete" />
                <el-option label="导出" value="export" />
                <el-option label="导入" value="import" />
                <el-option label="审核" value="audit" />
                <el-option label="发布" value="publish" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-radio-group v-model="formData.status" class="status-radio-group">
                <el-radio :value="1" class="status-radio">
                  <span class="radio-content">
                    <el-icon :color="'#10b981'"><CircleCheck /></el-icon>
                    启用
                  </span>
                </el-radio>
                <el-radio :value="0" class="status-radio">
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
            <el-form-item label="路径">
              <el-input v-model="formData.path" placeholder="访问路径" clearable>
                <template #prefix>
                  <el-icon><Location /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="请求方法">
              <el-select v-model="formData.method" placeholder="请求方法" clearable style="width: 100%">
                <el-option label="GET" value="GET" />
                <el-option label="POST" value="POST" />
                <el-option label="PUT" value="PUT" />
                <el-option label="DELETE" value="DELETE" />
                <el-option label="PATCH" value="PATCH" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="描述" prop="description">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入权限描述，说明该权限的用途和适用范围..."
            class="description-input"
          />
        </el-form-item>

        <el-divider content-position="left">
          <span class="divider-title">
            <el-icon><Star /></el-icon>
            快速模板
          </span>
        </el-divider>

        <div class="template-grid">
          <div class="template-card" @click="applyTemplate('view')">
            <div class="template-icon" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
              <el-icon :size="24"><View /></el-icon>
            </div>
            <div class="template-info">
              <div class="template-title">查看权限</div>
              <div class="template-desc">只读数据访问权限</div>
            </div>
          </div>
          <div class="template-card" @click="applyTemplate('create')">
            <div class="template-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
              <el-icon :size="24"><Plus /></el-icon>
            </div>
            <div class="template-info">
              <div class="template-title">新增权限</div>
              <div class="template-desc">可新增数据</div>
            </div>
          </div>
          <div class="template-card" @click="applyTemplate('manage')">
            <div class="template-icon" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);">
              <el-icon :size="24"><Tools /></el-icon>
            </div>
            <div class="template-info">
              <div class="template-title">管理权限</div>
              <div class="template-desc">完全数据管理权限</div>
            </div>
          </div>
        </div>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <div class="footer-left">
            <el-tag v-if="dialogType === 'edit'" type="info" size="small">
              <el-icon><InfoFilled /></el-icon>
              权限编码不可修改
            </el-tag>
          </div>
          <div class="footer-right">
            <el-button @click="dialogVisible = false" class="cancel-btn">
              <el-icon><Close /></el-icon>
              取消
            </el-button>
            <el-button type="primary" :loading="submitLoading" @click="handleSubmit" class="submit-btn">
              <el-icon><Check /></el-icon>
              {{ dialogType === 'create' ? '创建权限' : '保存修改' }}
            </el-button>
          </div>
        </div>
      </template>
    </el-dialog>

    <el-dialog
      v-model="rolesDialogVisible"
      title="关联角色"
      width="800px"
      class="roles-dialog"
      :close-on-click-modal="false"
    >
      <div class="roles-dialog-header">
        <div class="current-permission">
          <el-icon class="permission-icon"><Key /></el-icon>
          <div class="permission-info">
            <span class="permission-label">当前权限</span>
            <span class="permission-name">{{ currentPermissionName }}</span>
          </div>
        </div>
        <div class="roles-stats">
          <div class="stat-item">
            <span class="stat-label">关联角色</span>
            <span class="stat-value">{{ currentPermissionRoles.length }}</span>
          </div>
        </div>
      </div>

      <div class="roles-table-wrapper">
        <el-table :data="currentPermissionRoles" v-loading="rolesLoading" stripe class="modern-table">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="角色名称" min-width="180">
            <template #default="{ row }">
              <div class="cell-name">
                <div class="role-icon-mini" :style="{ background: (row as any).color || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }">
                  <el-icon><component :is="(row as any).icon || 'Key'" /></el-icon>
                </div>
                <div class="role-info-mini">
                  <div class="role-name-mini">{{ row.name }}</div>
                  <el-tag size="small" type="info">{{ row.code }}</el-tag>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="角色类型" width="120">
            <template #default="{ row }">
              <el-tag :type="getRoleTypeTagType(row.type)">
                {{ getRoleTypeLabel(row.type) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <div class="status-cell">
                <span class="status-dot" :class="row.status === 1 ? 'active' : 'inactive'"></span>
                <span>{{ row.status === 1 ? '启用' : '禁用' }}</span>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="rolesDialogVisible = false">关闭</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { permissionService } from '@/services'
import type { Permission, PermissionCreateRequest } from '@/types'
import { 
  Search, Refresh, Plus, Delete, Download, Edit, Key,
  Select, CircleCheck, CircleClose, UserFilled,
  Check, List, Setting, Document,
  InfoFilled, Close, Lock, Star, Trophy, Medal,
  Monitor, Tools, MagicStick, Timer, DataLine,
  Histogram, PieChart, TrendCharts, Warning, Bell, Message,
  Phone, OfficeBuilding, Position, Operation,
  Goods, ShoppingCart, Wallet, Ticket, Coin,
  Box, Files, Folder, Upload, RefreshLeft,
  RefreshRight, Share, Link, ScaleToOriginal, FullScreen,
  Minus, ArrowUp, ArrowDown, ArrowLeft,
  ArrowRight, Top, Bottom, Right, Sort,
  SortDown, SortUp, Filter, View, Connection, Location
} from '@element-plus/icons-vue'
import { exportToCSV } from '@/utils/export'
import { formatDate } from '@/utils/date'

const loading = ref(false)
const tableData = ref<Permission[]>([])
const allPermissions = ref<Permission[]>([])
const selectedIds = ref<number[]>([])
const rolesDialogVisible = ref(false)
const rolesLoading = ref(false)
const currentPermissionRoles = ref<any[]>([])
const currentPermissionName = ref('')

const availableIcons = [
  'Key', 'Lock', 'Star', 'Trophy', 'Medal',
  'Monitor', 'Tools', 'MagicStick', 'Timer',
  'DataLine', 'Histogram', 'PieChart', 'TrendCharts',
  'Warning', 'Bell', 'Message', 'Phone', 'OfficeBuilding',
  'Position', 'Operation', 'Goods',
  'ShoppingCart', 'Wallet', 'Ticket', 'Coin',
  'Box', 'Files', 'Folder', 'Upload', 'Download', 'RefreshLeft',
  'RefreshRight', 'Share', 'Link', 'ScaleToOriginal', 'FullScreen',
  'Setting', 'Menu', 'Connection', 'Location', 'View'
]

const predefinedColors = [
  '#667eea', '#764ba2', '#f093fb', '#f5576c',
  '#4facfe', '#00f2fe', '#43e97b', '#38f9d7',
  '#fa709a', '#fee140', '#a18cd1', '#fbc2eb',
  '#667eea', '#764ba2', '#ffecd2', '#fcb69f',
  '#ff9a9e', '#fecfef', '#a1c4fd', '#c2e9fb',
  '#d299c2', '#fef9d7', '#fccb90', '#ee9ca7'
]

const searchParams = reactive({
  keyword: '',
  type: undefined as number | undefined,
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
  name: '',
  code: '',
  description: '',
  type: 2 as number,
  resourceType: '',
  resourceId: undefined as string | number | undefined,
  action: '',
  path: '',
  method: undefined as string | undefined,
  parentId: undefined as number | undefined,
  status: 1,
  icon: 'Key' as string | undefined,
  color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' as string | undefined
})

const rules: FormRules = {
  name: [{ required: true, message: '请输入权限名称', trigger: 'blur' }],
  code: [{ required: true, message: '请输入权限编码', trigger: 'blur' }],
  type: [{ required: true, message: '请选择类型', trigger: 'change' }]
}

const permissionTree = computed(() => {
  return buildPermissionTree(allPermissions.value)
})

const buildPermissionTree = (permissions: Permission[]): Permission[] => {
  const map = new Map<number, Permission & { children: Permission[] }>()
  const roots: Permission[] = []

  permissions.forEach(perm => {
    map.set(perm.id, { ...perm, children: [] })
  })

  permissions.forEach(perm => {
    const node = map.get(perm.id)!
    if (perm.parentId && map.has(perm.parentId)) {
      map.get(perm.parentId)!.children.push(node)
    } else {
      roots.push(node)
    }
  })

  return roots
}

const getPermissionTypeLabel = (type: number): string => {
  const labels: Record<number, string> = {
    0: '菜单',
    1: '按钮',
    2: 'API',
    3: '数据',
    4: '字段'
  }
  return labels[type] || '未知'
}

const getPermissionTypeTagType = (type: number): 'success' | 'warning' | 'info' | 'danger' => {
  const tagMap: Record<number, 'success' | 'warning' | 'info' | 'danger'> = {
    0: 'danger',
    1: 'warning',
    2: 'info',
    3: 'success',
    4: 'success'
  }
  return tagMap[type] || 'success'
}

const getRoleTypeLabel = (type: number): string => {
  const labels: Record<number, string> = {
    0: '系统角色',
    1: '功能角色',
    2: '数据角色',
    3: '自定义角色'
  }
  return labels[type] || '未知'
}

const getRoleTypeTagType = (type: number): 'success' | 'warning' | 'info' | 'danger' => {
  const tagMap: Record<number, 'success' | 'warning' | 'info' | 'danger'> = {
    0: 'danger',
    1: 'warning',
    2: 'info',
    3: 'success'
  }
  return tagMap[type] || 'success'
}

const submitLoading = ref(false)

const loadData = async () => {
  loading.value = true
  try {
    const data = await permissionService.getPermissions({
      ...searchParams,
      page: pagination.page,
      pageSize: pagination.pageSize
    })
    tableData.value = data.items
    pagination.total = data.total
    
    await loadAllPermissions()
    await loadRoleCounts()
  } finally {
    loading.value = false
  }
}

const loadAllPermissions = async () => {
  try {
    allPermissions.value = await permissionService.getAllPermissions()
  } catch {
  }
}

const loadRoleCounts = async () => {
  try {
    for (const perm of tableData.value) {
      try {
        const result = await permissionService.countPermissionRoles(perm.id)
        ;(perm as any).roleCount = result.roleCount
      } catch {
        ;(perm as any).roleCount = 0
      }
    }
  } catch {
  }
}

const resetSearch = () => {
  searchParams.keyword = ''
  searchParams.type = undefined
  searchParams.status = undefined
  pagination.page = 1
  loadData()
}

const handleCreate = () => {
  dialogType.value = 'create'
  Object.assign(formData, {
    id: null,
    name: '',
    code: '',
    description: '',
    type: 2,
    resourceType: '',
    resourceId: undefined,
    action: '',
    path: '',
    method: undefined,
    parentId: undefined,
    status: 1,
    icon: 'Key',
    color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  })
  dialogVisible.value = true
}

const handleEdit = (row: Permission) => {
  dialogType.value = 'edit'
  Object.assign(formData, {
    id: row.id,
    name: row.name,
    code: row.code,
    description: row.description || '',
    type: row.type,
    resourceType: row.resourceType || '',
    resourceId: row.resourceId,
    action: row.action || '',
    path: row.path || '',
    method: row.method,
    parentId: row.parentId,
    status: row.status,
    icon: (row as any).icon || 'Key',
    color: (row as any).color || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  })
  dialogVisible.value = true
}

const applyTemplate = (type: string) => {
  switch (type) {
    case 'view':
      formData.name = formData.name || '查看权限'
      formData.code = formData.code || 'resource:view'
      formData.description = formData.description || '只读数据访问权限，可查看相关资源列表和详情'
      formData.action = 'view'
      formData.icon = 'View'
      formData.color = 'linear-gradient(135deg, #10b981 0%, #059669 100%)'
      ElMessage.success('已应用查看权限模板')
      break
    case 'create':
      formData.name = formData.name || '新增权限'
      formData.code = formData.code || 'resource:create'
      formData.description = formData.description || '新增数据权限，可创建新的资源记录'
      formData.action = 'create'
      formData.icon = 'Plus'
      formData.color = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
      ElMessage.success('已应用新增权限模板')
      break
    case 'manage':
      formData.name = formData.name || '管理权限'
      formData.code = formData.code || 'resource:manage'
      formData.description = formData.description || '完全数据管理权限，可查看、新增、编辑、删除相关资源'
      formData.action = 'manage'
      formData.icon = 'Tools'
      formData.color = 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)'
      ElMessage.success('已应用管理权限模板')
      break
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitLoading.value = true
      try {
        const requestData: any = {
          name: formData.name,
          code: formData.code,
          description: formData.description,
          type: Number(formData.type),
          resource_type: formData.resourceType,
          action: formData.action,
          path: formData.path,
          method: formData.method,
          parent_id: formData.parentId != null ? Number(formData.parentId) : null,
          status: Number(formData.status),
          icon: formData.icon,
          color: formData.color
        }
        
        if (dialogType.value === 'create') {
          await permissionService.createPermission(requestData as PermissionCreateRequest)
          ElMessage.success('创建成功')
        } else {
          await permissionService.updatePermission(formData.id!, requestData)
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

const handleDelete = async (row: Permission) => {
  try {
    await ElMessageBox.confirm('确定要删除该权限吗?', '提示', {
      type: 'warning'
    })
    await permissionService.deletePermission(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch {
  }
}

const handleViewRoles = async (row: Permission) => {
  currentPermissionName.value = row.name
  rolesDialogVisible.value = true
  rolesLoading.value = true
  try {
    const result = await permissionService.getPermissionRoles(row.id)
    currentPermissionRoles.value = result.roles || []
  } finally {
    rolesLoading.value = false
  }
}

const handleSelectionChange = (selection: Permission[]) => {
  selectedIds.value = selection.map(item => item.id)
}

const handleBatchEnable = async () => {
  try {
    await ElMessageBox.confirm(`确定要启用选中的 ${selectedIds.value.length} 个权限吗?`, '提示', {
      type: 'success'
    })
    const promises = selectedIds.value.map(id => permissionService.updatePermissionStatus(id, 1))
    await Promise.all(promises)
    ElMessage.success('批量启用成功')
    selectedIds.value = []
    loadData()
  } catch {
  }
}

const handleBatchDisable = async () => {
  try {
    await ElMessageBox.confirm(`确定要禁用选中的 ${selectedIds.value.length} 个权限吗?`, '提示', {
      type: 'warning'
    })
    const promises = selectedIds.value.map(id => permissionService.updatePermissionStatus(id, 0))
    await Promise.all(promises)
    ElMessage.success('批量禁用成功')
    selectedIds.value = []
    loadData()
  } catch {
  }
}

const handleBatchDelete = async () => {
  try {
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedIds.value.length} 个权限吗?`, '提示', {
      type: 'warning'
    })
    const promises = selectedIds.value.map(id => permissionService.deletePermission(id))
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
    { key: 'name', title: '权限名称' },
    { key: 'code', title: '权限编码' },
    { key: 'type', title: '类型' },
    { key: 'resourceType', title: '资源类型' },
    { key: 'action', title: '操作' },
    { key: 'path', title: '路径' },
    { key: 'status', title: '状态' }
  ]
  
  const exportData = tableData.value.map(item => ({
    ...item,
    type: getPermissionTypeLabel(item.type),
    status: item.status === 1 ? '启用' : '禁用'
  }))
  
  const filename = `权限数据_${formatDate(new Date(), 'YYYY-MM-DD')}`
  exportToCSV(exportData, filename, headers)
  ElMessage.success('导出成功')
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';

.permission-list-page {
  padding: 24px;
  background: $background-page;
  min-height: calc(100vh - 60px);

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

          .permission-icon-mini {
            width: 44px;
            height: 44px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            flex-shrink: 0;

            .el-icon {
              font-size: 22px;
            }
          }

          .permission-info-mini {
            display: flex;
            flex-direction: column;
            gap: 4px;

            .permission-name-mini {
              font-size: 14px;
              font-weight: 600;
              color: $text-primary;
            }
          }

          .role-icon-mini {
            width: 44px;
            height: 44px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            flex-shrink: 0;

            .el-icon {
              font-size: 22px;
            }
          }

          .role-info-mini {
            display: flex;
            flex-direction: column;
            gap: 4px;

            .role-name-mini {
              font-size: 14px;
              font-weight: 600;
              color: $text-primary;
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

  .permission-dialog {
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

    .permission-profile-section {
      padding: 28px;
      background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
      border-bottom: 1px solid $border-lighter;

      .profile-header {
        display: flex;
        align-items: center;
        gap: 24px;

        .permission-icon-section {
          .permission-icon-display {
            width: 90px;
            height: 90px;
            border-radius: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
          }
        }

        .permission-info-section {
          display: flex;
          flex-direction: column;
          gap: 8px;

          .permission-name-display {
            font-size: 26px;
            font-weight: 700;
            color: $text-primary;
          }

          .permission-code-display {
            font-size: 14px;
            color: $text-secondary;
          }

          .permission-status {
            display: flex;
            gap: 8px;
          }
        }
      }
    }

    .template-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin-top: 8px;

      .template-card {
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

        .template-icon {
          width: 48px;
          height: 48px;
          border-radius: $border-radius-lg;
          display: flex;
          align-items: center;
          justify-content: center;
          color: #fff;
          flex-shrink: 0;
        }

        .template-info {
          flex: 1;

          .template-title {
            font-size: 15px;
            font-weight: 600;
            color: $text-primary;
            margin-bottom: 2px;
          }

          .template-desc {
            font-size: 12px;
            color: $text-secondary;
          }
        }
      }
    }

    .permission-form {
      padding: 24px;

      .divider-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 600;
        color: $text-primary;
      }

      .description-input {
        :deep(.el-textarea__inner) {
          border-radius: $border-radius-md;
          resize: none;
        }
      }

      .icon-option {
        display: flex;
        align-items: center;
        gap: 8px;

        .el-icon {
          color: $primary-color;
        }
      }

      .color-picker-wrapper {
        display: flex;
        align-items: center;
        gap: 12px;

        .color-preview {
          width: 40px;
          height: 40px;
          border-radius: $border-radius-md;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
      }

      .status-radio-group {
        display: flex;
        gap: 16px;

        .status-radio {
          .radio-content {
            display: flex;
            align-items: center;
            gap: 6px;
          }
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

            &.el-button--primary {
              background: $gradient-primary;
              border: none;
              box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            }
          }
        }
      }
    }
  }

  .roles-dialog {
    :deep(.el-dialog__header) {
      padding: 20px 24px 16px;
      border-bottom: 1px solid $border-lighter;
    }

    :deep(.el-dialog__body) {
      padding: 24px;
    }

    .roles-dialog-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      padding: 16px 20px;
      background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
      border-radius: $border-radius-lg;
      border: 1px solid $border-lighter;

      .current-permission {
        display: flex;
        align-items: center;
        gap: 12px;

        .permission-icon {
          color: $primary-color;
        }

        .permission-info {
          display: flex;
          flex-direction: column;
          gap: 4px;

          .permission-label {
            font-size: 12px;
            color: $text-secondary;
            margin-bottom: 2px;
          }

          .permission-name {
            font-size: 16px;
            font-weight: 600;
            color: $text-primary;
          }
        }
      }

      .roles-stats {
        display: flex;
        gap: 24px;

        .stat-item {
          display: flex;
          flex-direction: column;
          align-items: flex-end;

          .stat-label {
            font-size: 12px;
            color: $text-secondary;
            margin-bottom: 2px;
          }

          .stat-value {
            font-size: 20px;
            font-weight: 700;
            background: $gradient-primary;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
          }
        }
      }
    }

    .roles-table-wrapper {
      margin-top: 20px;
    }
  }
}
</style>
