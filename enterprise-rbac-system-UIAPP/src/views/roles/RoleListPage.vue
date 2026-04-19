<template>
  <div class="role-list-page">
    <div class="page-header">
      <div class="header-left">
        <el-icon class="header-icon" :size="28"><UserFilled /></el-icon>
        <div class="header-title">
          <h1>角色管理</h1>
          <p>管理系统中的角色和权限分配</p>
        </div>
      </div>
      <div class="header-right">
        <el-button :icon="Refresh" @click="loadData" class="icon-btn">
          刷新
        </el-button>
        <el-button type="primary" :icon="Plus" @click="handleCreate" class="primary-btn" v-permission="'role:create'">
          新增角色
        </el-button>
      </div>
    </div>

    <el-card class="main-card" shadow="never">
      <div class="card-content">
        <div class="search-bar">
          <div class="search-items">
            <el-input
              v-model="searchParams.keyword"
              placeholder="搜索角色名称/编码"
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
            <el-button type="danger" :icon="Delete" @click="handleBatchDelete" v-permission="'role:delete'">
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
            <el-table-column prop="name" label="角色名称" min-width="220">
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
            <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
            <el-table-column label="角色类型" width="120">
              <template #default="{ row }">
                <el-tag :type="getRoleTypeTag((row as any).type)">
                  {{ getRoleTypeName((row as any).type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="sort" label="排序" width="100" />
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
                    v-permission="'role:update'"
                  >
                    <el-icon><Edit /></el-icon>
                    编辑
                  </el-button>
                  <el-button
                    link
                    type="primary"
                    size="small"
                    :loading="assignPermissionLoading && currentRoleId === row.id"
                    @click="handleAssignPermissions(row)"
                    v-permission="'role:update'"
                  >
                    <el-icon><Key /></el-icon>
                    权限
                  </el-button>
                  <el-button
                    link
                    type="danger"
                    size="small"
                    @click="handleDelete(row)"
                    v-permission="'role:delete'"
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
      :title="dialogType === 'create' ? '新增角色' : '编辑角色'"
      width="750px"
      :close-on-click-modal="false"
      class="role-dialog"
    >
      <div class="role-profile-section">
        <div class="profile-header">
          <div class="role-icon-section">
            <div class="role-icon-display" :style="{ background: formData.color || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }">
              <el-icon :size="44"><component :is="formData.icon || 'Key'" /></el-icon>
            </div>
          </div>
          <div class="role-info-section">
            <div class="role-name-display">{{ formData.name || '角色名称' }}</div>
            <div class="role-code-display">{{ formData.code || 'ROLE_CODE' }}</div>
            <div class="role-status">
              <el-tag size="small" :type="formData.status === 1 ? 'success' : 'danger'">
                {{ formData.status === 1 ? '启用' : '禁用' }}
              </el-tag>
            </div>
          </div>
        </div>
      </div>

      <el-form ref="formRef" :model="formData" :rules="rules" label-width="100px" class="role-form">
        <el-divider content-position="left">
          <span class="divider-title">
            <el-icon><Setting /></el-icon>
            基本信息
          </span>
        </el-divider>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="角色名称" prop="name">
              <el-input v-model="formData.name" placeholder="请输入角色名称" clearable>
                <template #prefix>
                  <el-icon><User /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="角色编码" prop="code">
              <el-input v-model="formData.code" placeholder="请输入角色编码" :disabled="dialogType === 'edit'" clearable>
                <template #prefix>
                  <el-icon><Key /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="角色类型" prop="type">
              <el-select v-model="formData.type" placeholder="选择角色类型" style="width: 100%">
                <el-option 
                  v-for="item in roleTypeOptions" 
                  :key="item.value" 
                  :value="typeof item.value === 'string' ? Number(item.value) : item.value" 
                  :label="item.label" 
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="数据范围" prop="dataScope">
              <el-select v-model="formData.dataScope" placeholder="选择数据范围" style="width: 100%">
                <el-option 
                  v-for="item in dataScopeOptions" 
                  :key="item.value" 
                  :value="typeof item.value === 'string' ? Number(item.value) : item.value" 
                  :label="item.label" 
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="父角色">
              <el-select 
                v-model="formData.parentId" 
                placeholder="选择父角色" 
                clearable
                style="width: 100%"
              >
                <el-option 
                  v-for="role in tableData" 
                  :key="role.id"
                  :label="role.name" 
                  :value="role.id"
                  :disabled="role.id === formData.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="角色颜色">
              <div class="color-picker-wrapper">
                <el-color-picker 
                  v-model="formData.color" 
                  show-alpha
                  :predefine="predefinedColors"
                  popper-class="role-color-picker"
                />
                <div class="color-preview" :style="{ background: formData.color || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }"></div>
              </div>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="角色图标">
              <el-select v-model="formData.icon" placeholder="选择角色图标" clearable style="width: 100%">
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

        <el-form-item label="描述" prop="description">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入角色描述，说明该角色的用途和权限范围..."
            class="description-input"
          />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="排序" prop="sort">
              <el-input-number 
                v-model="formData.sort" 
                :min="0" 
                :max="999"
                style="width: 100%"
                controls-position="right"
              />
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

        <el-divider content-position="left">
          <span class="divider-title">
            <el-icon><Star /></el-icon>
            快速模板
          </span>
        </el-divider>

        <div class="template-grid">
          <div class="template-card" @click="applyTemplate('admin')">
            <div class="template-icon" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);">
              <el-icon :size="24"><Trophy /></el-icon>
            </div>
            <div class="template-info">
              <div class="template-title">超级管理员</div>
              <div class="template-desc">拥有全部系统权限</div>
            </div>
          </div>
          <div class="template-card" @click="applyTemplate('editor')">
            <div class="template-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
              <el-icon :size="24"><Edit /></el-icon>
            </div>
            <div class="template-info">
              <div class="template-title">内容编辑</div>
              <div class="template-desc">可编辑内容数据</div>
            </div>
          </div>
          <div class="template-card" @click="applyTemplate('viewer')">
            <div class="template-icon" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
              <el-icon :size="24"><View /></el-icon>
            </div>
            <div class="template-info">
              <div class="template-title">数据查看</div>
              <div class="template-desc">只读权限</div>
            </div>
          </div>
        </div>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <div class="footer-left">
            <el-tag v-if="dialogType === 'edit'" type="info" size="small">
              <el-icon><InfoFilled /></el-icon>
              角色编码不可修改
            </el-tag>
          </div>
          <div class="footer-right">
            <el-button @click="dialogVisible = false" class="cancel-btn">
              <el-icon><Close /></el-icon>
              取消
            </el-button>
            <el-button type="primary" :loading="submitLoading" @click="handleSubmit" class="submit-btn">
              <el-icon><Check /></el-icon>
              {{ dialogType === 'create' ? '创建角色' : '保存修改' }}
            </el-button>
          </div>
        </div>
      </template>
    </el-dialog>

    <el-dialog
      v-model="permissionDialogVisible"
      :key="permissionDialogKey"
      title="分配权限"
      width="800px"
      class="permission-dialog"
      :close-on-click-modal="false"
    >
      <div class="permission-dialog-header">
        <div class="current-role">
          <el-icon class="role-icon"><Key /></el-icon>
          <div class="role-info">
            <span class="role-label">当前角色</span>
            <span class="role-name">{{ currentRoleName }}</span>
          </div>
        </div>
        <div class="permission-stats">
          <div class="stat-item">
            <span class="stat-label">已选权限</span>
            <span class="stat-value">{{ checkedCount }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">总权限数</span>
            <span class="stat-value">{{ totalCount }}</span>
          </div>
        </div>
      </div>

      <div class="permission-toolbar">
        <div class="toolbar-left">
          <el-input
            v-model="permissionSearch"
            placeholder="搜索权限名称/编码..."
            :prefix-icon="Search"
            clearable
            class="search-input"
          />
          <el-select
            v-model="permissionTypeFilter"
            placeholder="权限类型"
            clearable
            class="type-select"
          >
            <el-option :value="0" label="菜单权限" />
            <el-option :value="1" label="按钮权限" />
            <el-option :value="2" label="API权限" />
            <el-option :value="3" label="数据权限" />
            <el-option :value="4" label="字段权限" />
          </el-select>
        </div>
        <div class="toolbar-right">
          <el-button :icon="Expand" @click="expandAll">展开全部</el-button>
          <el-button :icon="Fold" @click="collapseAll">收起全部</el-button>
          <el-button type="primary" :icon="List" @click="checkAll">全选</el-button>
          <el-button :icon="Delete" @click="uncheckAll">清空</el-button>
        </div>
      </div>

      <div class="permission-tree-wrapper">
        <el-tree
          ref="permissionTreeRef"
          :data="filteredPermissions"
          :props="{ label: 'name', value: 'id', children: 'children' }"
          show-checkbox
          node-key="id"
          :default-checked-keys="selectedPermissionIds"
          :default-expand-all="true"
          @check="handlePermissionCheck"
          class="permission-tree"
        >
          <template #default="{ node, data }">
            <div class="tree-node-content">
              <div
                class="permission-icon-mini"
                :style="{ background: (data as any).color || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }"
              >
                <el-icon>
                  <component :is="(data as any).icon || 'Key'" />
                </el-icon>
              </div>
              <div class="permission-info-mini">
                <div class="permission-name-mini">{{ node.label }}</div>
                <div class="permission-meta">
                  <el-tag size="small" type="info" class="code-tag">
                    {{ (data as any).code }}
                  </el-tag>
                  <el-tag
                    v-if="(data as any).type !== undefined"
                    size="small"
                    :type="getPermissionTypeTagType((data as any).type)"
                    class="type-tag"
                  >
                    {{ getPermissionTypeLabel((data as any).type) }}
                  </el-tag>
                </div>
              </div>
            </div>
          </template>
        </el-tree>
      </div>

      <div class="permission-summary" v-if="selectedPermissionCount > 0">
        <div class="summary-title">
          <el-icon><Document /></el-icon>
          <span>已选择权限概览</span>
        </div>
        <div class="summary-stats">
          <div class="stat-item">
            <el-tag size="small" type="success">
              菜单权限: {{ permissionStats.menu }}
            </el-tag>
          </div>
          <div class="stat-item">
            <el-tag size="small" type="warning">
              按钮权限: {{ permissionStats.button }}
            </el-tag>
          </div>
          <div class="stat-item">
            <el-tag size="small" type="info">
              API权限: {{ permissionStats.api }}
            </el-tag>
          </div>
          <div class="stat-item">
            <el-tag size="small" type="danger">
              数据权限: {{ permissionStats.data }}
            </el-tag>
          </div>
          <div class="stat-item">
            <el-tag size="small">
              字段权限: {{ permissionStats.field }}
            </el-tag>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <div class="footer-left">
            <el-tag type="info">
              提示：勾选父节点会自动勾选所有子节点
            </el-tag>
          </div>
          <div class="footer-right">
            <el-button @click="permissionDialogVisible = false">取消</el-button>
            <el-button type="primary" :loading="permissionSubmitLoading" @click="handlePermissionSubmit">
              <el-icon><Check /></el-icon>
              保存权限
            </el-button>
          </div>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { roleService, permissionService, systemDictService } from '@/services'
import type { Role, RoleCreateRequest, RoleUpdateRequest, Permission } from '@/types'
import type { DictItemSimple } from '@/services/systemDict'
import { 
  Search, Refresh, Plus, Delete, Download, Edit, Key,
  Select, CircleCheck, CircleClose, UserFilled,
  Expand, Fold, Check, List, Setting, User, Document,
  InfoFilled, Close, Lock, Star, Trophy, Medal,
  Monitor, Tools, MagicStick, Timer, DataLine,
  Histogram, PieChart, TrendCharts, Warning, Bell, Message,
  Phone, OfficeBuilding, Position, Operation,
  Goods, ShoppingCart, Wallet, Ticket, Coin,
  Box, Files, Folder, Upload, RefreshLeft,
  RefreshRight, Share, Link, ScaleToOriginal, FullScreen,
  ArrowUp, ArrowDown, ArrowLeft,
  ArrowRight, Top, Bottom, Right, Sort,
  SortDown, SortUp, Filter, View
} from '@element-plus/icons-vue'
import { exportToCSV, buildTree } from '@/utils/export'
import { formatDate } from '@/utils/date'

const loading = ref(false)
const tableData = ref<Role[]>([])
const allPermissions = ref<Permission[]>([])
const selectedPermissionIds = ref<number[]>([])
const currentRoleId = ref<number | null>(null)
const currentRoleName = ref('')
const permissionSearch = ref('')
const selectedIds = ref<number[]>([])
const roleTypeOptions = ref<DictItemSimple[]>([])
const dataScopeOptions = ref<DictItemSimple[]>([])

const availableIcons = [
  'Key', 'Lock', 'User', 'UserFilled', 'Star',
  'Trophy', 'Medal', 'Monitor', 'Tools', 'MagicStick',
  'Timer', 'DataLine', 'Histogram', 'PieChart', 'TrendCharts',
  'Warning', 'Bell', 'Message', 'Phone', 'OfficeBuilding',
  'Position', 'Operation', 'Goods', 'ShoppingCart',
  'Wallet', 'Ticket', 'Coin', 'Box', 'Files',
  'Folder', 'Upload', 'Download', 'RefreshLeft', 'RefreshRight',
  'Share', 'Link', 'ScaleToOriginal', 'FullScreen', 'Setting'
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
  sort: 0,
  status: 1,
  icon: 'Key' as string | undefined,
  color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' as string | undefined,
  type: 3 as number,
  dataScope: 0 as number,
  parentId: undefined as number | undefined
})

const rules: FormRules = {
  name: [{ required: true, message: '请输入角色名称', trigger: 'blur' }],
  code: [{ required: true, message: '请输入角色编码', trigger: 'blur' }]
}

const getRoleTypeName = (type: number): string => {
  const option = roleTypeOptions.value.find(item => {
    const itemValue = typeof item.value === 'string' ? Number(item.value) : item.value
    return itemValue === type
  })
  if (option) {
    return option.label
  }
  const typeMap: Record<number, string> = {
    0: '系统角色',
    1: '功能角色',
    2: '数据角色',
    3: '自定义角色'
  }
  return typeMap[type] || '自定义角色'
}

const getRoleTypeTag = (type: number): 'success' | 'warning' | 'info' | 'danger' => {
  const tagMap: Record<number, 'success' | 'warning' | 'info' | 'danger'> = {
    0: 'danger',
    1: 'warning',
    2: 'info',
    3: 'success'
  }
  return tagMap[type] || 'success'
}

const getDataScopeName = (dataScope: number): string => {
  const option = dataScopeOptions.value.find(item => {
    const itemValue = typeof item.value === 'string' ? Number(item.value) : item.value
    return itemValue === dataScope
  })
  if (option) {
    return option.label
  }
  const scopeMap: Record<number, string> = {
    0: '全部数据',
    1: '本部门数据',
    2: '本部门及下级数据',
    3: '仅本人数据',
    4: '自定义数据'
  }
  return scopeMap[dataScope] || '全部数据'
}

const getPermissionTypeLabel = (type: number): string => {
  const typeMap: Record<number, string> = {
    0: '菜单权限',
    1: '按钮权限',
    2: 'API权限',
    3: '数据权限',
    4: '字段权限'
  }
  return typeMap[type] || '其他'
}

const getPermissionTypeTagType = (type: number): 'success' | 'warning' | 'info' | 'danger' | '' => {
  const tagMap: Record<number, 'success' | 'warning' | 'info' | 'danger' | ''> = {
    0: 'success',
    1: 'warning',
    2: 'info',
    3: 'danger',
    4: ''
  }
  return tagMap[type] || ''
}

const permissionDialogVisible = ref(false)
const permissionTreeRef = ref()
const submitLoading = ref(false)
const permissionSubmitLoading = ref(false)
const permissionTypeFilter = ref<number | undefined>()
const assignPermissionLoading = ref(false)
const permissionDialogKey = ref(0)

const loadData = async () => {
  loading.value = true
  try {
    const data = await roleService.getRoles({
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

const loadDicts = async () => {
  try {
    const roleTypeData = await systemDictService.getDictItemsByCode('role_type')
    roleTypeOptions.value = roleTypeData || []
    const dataScopeData = await systemDictService.getDictItemsByCode('data_scope')
    dataScopeOptions.value = dataScopeData || []
  } catch (error) {
    console.error('加载字典失败:', error)
  }
}

const resetSearch = () => {
  searchParams.keyword = ''
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
    sort: 0,
    status: 1,
    icon: 'Key',
    color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    type: 3,
    dataScope: 0,
    parentId: undefined
  })
  dialogVisible.value = true
}

const handleEdit = (row: Role) => {
  dialogType.value = 'edit'
  Object.assign(formData, {
    id: row.id,
    name: row.name,
    code: row.code,
    description: row.description || '',
    sort: row.sort,
    status: row.status,
    icon: (row as any).icon || 'Key',
    color: (row as any).color || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    type: (row as any).type !== undefined && (row as any).type !== null ? (row as any).type : 3,
    dataScope: (row as any).dataScope !== undefined && (row as any).dataScope !== null ? (row as any).dataScope : 0,
    parentId: (row as any).parentId
  })
  dialogVisible.value = true
}

const applyTemplate = (type: string) => {
  switch (type) {
    case 'admin':
      formData.name = formData.name || '超级管理员'
      formData.code = formData.code || 'SUPER_ADMIN'
      formData.description = formData.description || '拥有系统全部操作权限，可管理所有模块和用户'
      formData.icon = 'Trophy'
      formData.color = 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)'
      ElMessage.success('已应用超级管理员模板')
      break
    case 'editor':
      formData.name = formData.name || '内容编辑'
      formData.code = formData.code || 'CONTENT_EDITOR'
      formData.description = formData.description || '可编辑和管理内容数据，查看基础信息'
      formData.icon = 'Edit'
      formData.color = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
      ElMessage.success('已应用内容编辑模板')
      break
    case 'viewer':
      formData.name = formData.name || '数据查看'
      formData.code = formData.code || 'DATA_VIEWER'
      formData.description = formData.description || '只读权限，仅可查看系统数据和报表'
      formData.icon = 'View'
      formData.color = 'linear-gradient(135deg, #10b981 0%, #059669 100%)'
      ElMessage.success('已应用数据查看模板')
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
          sort: Number(formData.sort),
          status: Number(formData.status),
          type: Number(formData.type),
          data_scope: Number(formData.dataScope),
          parent_id: formData.parentId != null ? Number(formData.parentId) : null,
          icon: formData.icon,
          color: formData.color
        }
        
        if (dialogType.value === 'create') {
          await roleService.createRole(requestData as RoleCreateRequest)
          ElMessage.success('创建成功')
        } else {
          await roleService.updateRole(formData.id!, requestData as RoleUpdateRequest)
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        loadData()
      } catch (error: any) {
        console.error('保存失败:', error)
        ElMessage.error(error.message || '保存失败')
      } finally {
        submitLoading.value = false
      }
    }
  })
}

const handleDelete = async (row: Role) => {
  try {
    await ElMessageBox.confirm('确定要删除该角色吗?', '提示', {
      type: 'warning'
    })
    await roleService.deleteRole(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch {
  }
}

const handleAssignPermissions = async (row: Role) => {
  if (assignPermissionLoading.value) return
  
  assignPermissionLoading.value = true
  
  try {
    currentRoleId.value = row.id
    currentRoleName.value = row.name
    permissionSearch.value = ''
    permissionTypeFilter.value = undefined
    selectedPermissionIds.value = []
    
    permissionDialogKey.value++
    
    await loadAllPermissions()
    
    const result = await roleService.getRolePermissions(row.id) as any
    const perms = result?.permissions || []
    selectedPermissionIds.value = perms.map((p: any) => p.id)
    
    permissionDialogVisible.value = true
  } finally {
    assignPermissionLoading.value = false
  }
}

const loadAllPermissions = async () => {
  const permissions = await permissionService.getAllPermissions() as any[]
  const convertedPermissions = permissions.map(p => ({
    ...p,
    parentId: p.parent_id
  }))
  allPermissions.value = buildTree(convertedPermissions)
}

const getAllPermissionIds = (permissions: any[]): number[] => {
  let ids: number[] = []
  permissions.forEach(perm => {
    ids.push(perm.id)
    if (perm.children && perm.children.length > 0) {
      ids = ids.concat(getAllPermissionIds(perm.children))
    }
  })
  return ids
}

const filterPermissions = (permissions: any[], keyword: string, typeFilter?: number): any[] => {
  return permissions.filter(perm => {
    const matchKeyword = !keyword || 
      perm.name.toLowerCase().includes(keyword.toLowerCase()) || 
      (perm.code && perm.code.toLowerCase().includes(keyword.toLowerCase()))
    
    const matchType = typeFilter === undefined || perm.type === typeFilter
    
    const hasChildren = perm.children && perm.children.length > 0
    const filteredChildren = hasChildren ? filterPermissions(perm.children, keyword, typeFilter) : []
    
    const childrenMatch = hasChildren && filteredChildren.length > 0
    
    if ((matchKeyword && matchType) || childrenMatch) {
      return {
        ...perm,
        children: filteredChildren
      }
    }
    return false
  }).filter(Boolean)
}

const filteredPermissions = computed(() => {
  return filterPermissions(allPermissions.value, permissionSearch.value, permissionTypeFilter.value)
})

const totalCount = computed(() => {
  return getAllPermissionIds(allPermissions.value).length
})

const checkedCount = computed(() => {
  if (!permissionTreeRef.value) return 0
  const checkedKeys = permissionTreeRef.value.getCheckedKeys()
  return checkedKeys.length
})

const getSelectedPermissions = (): any[] => {
  if (!permissionTreeRef.value || !allPermissions.value) return []
  const checkedKeys = permissionTreeRef.value.getCheckedKeys()
  const collectPermissions = (permissions: any[]): any[] => {
    let result: any[] = []
    permissions.forEach(perm => {
      if (checkedKeys.includes(perm.id)) {
        result.push(perm)
      }
      if (perm.children && perm.children.length > 0) {
        result = result.concat(collectPermissions(perm.children))
      }
    })
    return result
  }
  return collectPermissions(allPermissions.value)
}

const selectedPermissionCount = computed(() => {
  return checkedCount.value
})

const permissionStats = computed(() => {
  const permissions = getSelectedPermissions()
  const stats = {
    menu: 0,
    button: 0,
    api: 0,
    data: 0,
    field: 0
  }
  
  permissions.forEach(perm => {
    switch (perm.type) {
      case 0:
        stats.menu++
        break
      case 1:
        stats.button++
        break
      case 2:
        stats.api++
        break
      case 3:
        stats.data++
        break
      case 4:
        stats.field++
        break
    }
  })
  
  return stats
})

const handlePermissionCheck = () => {
}

const expandAll = () => {
  if (!permissionTreeRef.value) return
  permissionTreeRef.value.store.nodesMap && Object.values(permissionTreeRef.value.store.nodesMap).forEach((node: any) => {
    node.expanded = true
  })
}

const collapseAll = () => {
  if (!permissionTreeRef.value) return
  permissionTreeRef.value.store.nodesMap && Object.values(permissionTreeRef.value.store.nodesMap).forEach((node: any) => {
    node.expanded = false
  })
}

const checkAll = () => {
  const allIds = getAllPermissionIds(allPermissions.value)
  selectedPermissionIds.value = allIds
  setTimeout(() => {
    if (permissionTreeRef.value) {
      permissionTreeRef.value.setCheckedKeys(allIds)
    }
  }, 100)
}

const uncheckAll = () => {
  selectedPermissionIds.value = []
  setTimeout(() => {
    if (permissionTreeRef.value) {
      permissionTreeRef.value.setCheckedKeys([])
    }
  }, 100)
}

const handlePermissionSubmit = async () => {
  if (!permissionTreeRef.value || !currentRoleId.value) return
  const checkedKeys = permissionTreeRef.value.getCheckedKeys()
  permissionSubmitLoading.value = true
  try {
    await roleService.assignPermissions(currentRoleId.value, { permission_ids: checkedKeys } as any)
    ElMessage.success('分配成功')
    permissionDialogVisible.value = false
    loadData()
  } finally {
    permissionSubmitLoading.value = false
  }
}

const handleSelectionChange = (selection: Role[]) => {
  selectedIds.value = selection.map(item => item.id)
}

const handleBatchEnable = async () => {
  try {
    await ElMessageBox.confirm(`确定要启用选中的 ${selectedIds.value.length} 个角色吗?`, '提示', {
      type: 'success'
    })
    const promises = selectedIds.value.map(id => roleService.updateRole(id, { status: 1 }))
    await Promise.all(promises)
    ElMessage.success('批量启用成功')
    selectedIds.value = []
    loadData()
  } catch {
  }
}

const handleBatchDisable = async () => {
  try {
    await ElMessageBox.confirm(`确定要禁用选中的 ${selectedIds.value.length} 个角色吗?`, '提示', {
      type: 'warning'
    })
    const promises = selectedIds.value.map(id => roleService.updateRole(id, { status: 0 }))
    await Promise.all(promises)
    ElMessage.success('批量禁用成功')
    selectedIds.value = []
    loadData()
  } catch {
  }
}

const handleBatchDelete = async () => {
  try {
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedIds.value.length} 个角色吗?`, '提示', {
      type: 'warning'
    })
    const promises = selectedIds.value.map(id => roleService.deleteRole(id))
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
    { key: 'name', title: '角色名称' },
    { key: 'code', title: '角色编码' },
    { key: 'description', title: '描述' },
    { key: 'sort', title: '排序' },
    { key: 'status', title: '状态' }
  ]
  
  const exportData = tableData.value.map(item => ({
    ...item,
    status: item.status === 1 ? '启用' : '禁用'
  }))
  
  const filename = `角色数据_${formatDate(new Date(), 'YYYY-MM-DD')}`
  exportToCSV(exportData, filename, headers)
  ElMessage.success('导出成功')
}

onMounted(() => {
  loadData()
  loadDicts()
})
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';

.role-list-page {
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

  .modern-dialog {
    :deep(.el-dialog__header) {
      padding: 20px 24px 16px;
      border-bottom: 1px solid $border-lighter;
    }

    :deep(.el-dialog__body) {
      padding: 24px;
    }

    :deep(.el-dialog__footer) {
      padding: 16px 24px 20px;
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

    .role-profile-section {
      padding: 28px;
      background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
      border-bottom: 1px solid $border-lighter;

      .profile-header {
        display: flex;
        align-items: center;
        gap: 24px;

        .role-icon-section {
          .role-icon-display {
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

        .role-info-section {
          display: flex;
          flex-direction: column;
          gap: 8px;

          .role-name-display {
            font-size: 26px;
            font-weight: 700;
            color: $text-primary;
          }

          .role-code-display {
            font-size: 14px;
            color: $text-secondary;
          }

          .role-status {
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

    .role-form {
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

    .permission-summary {
      padding: 16px 24px;
      background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
      border-top: 1px solid $border-lighter;

      .summary-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 14px;
        font-weight: 600;
        color: $text-primary;
        margin-bottom: 12px;

        .el-icon {
          color: $primary-color;
        }
      }

      .summary-stats {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;

        .stat-item {
          display: flex;
          align-items: center;
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

  .permission-tree {
    max-height: 400px;
    overflow-y: auto;
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

    .permission-dialog-header {
      padding: 20px 24px;
      background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
      border-bottom: 1px solid $border-lighter;
      display: flex;
      justify-content: space-between;
      align-items: center;

      .current-role {
        display: flex;
        align-items: center;
        gap: 12px;

        .role-icon {
          width: 40px;
          height: 40px;
          background: $gradient-primary;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          color: #fff;
          font-size: 20px;
        }

        .role-info {
          display: flex;
          flex-direction: column;

          .role-label {
            font-size: 12px;
            color: $text-secondary;
            margin-bottom: 2px;
          }

          .role-name {
            font-size: 16px;
            font-weight: 600;
            color: $text-primary;
          }
        }
      }

      .permission-stats {
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

    .permission-toolbar {
      padding: 16px 24px;
      background: #fff;
      border-bottom: 1px solid $border-lighter;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;

      .toolbar-left {
        display: flex;
        gap: 12px;

        .search-input {
          width: 280px;

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

        .type-select {
          width: 140px;

          :deep(.el-select__wrapper) {
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

        .el-button {
          border-radius: $border-radius-md;
          font-weight: 500;
          transition: all 0.3s;

          &:hover {
            transform: translateY(-1px);
          }

          &.el-button--primary {
            background: $gradient-primary;
            border: none;
          }
        }
      }
    }

    .permission-tree-wrapper {
      padding: 24px;
      max-height: 400px;
      overflow-y: auto;

      .permission-tree {
        :deep(.el-tree-node__content) {
          height: auto;
          min-height: 56px;
          border-radius: $border-radius-md;
          transition: all 0.2s;
          margin-bottom: 4px;
          padding: 8px 12px;

          &:hover {
            background: rgba(102, 126, 234, 0.05);
          }
        }

        :deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
          background: $gradient-primary;
          border-color: transparent;
        }

        :deep(.el-checkbox__input.is-indeterminate .el-checkbox__inner) {
          background: #667eea;
          border-color: transparent;
        }

        .tree-node-content {
          display: flex;
          align-items: center;
          gap: 12px;
          flex: 1;
          padding-left: 4px;

          .permission-icon-mini {
            width: 36px;
            height: 36px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
            box-shadow: 0 3px 8px rgba(0, 0, 0, 0.12);
            flex-shrink: 0;

            .el-icon {
              font-size: 18px;
            }
          }

          .permission-info-mini {
            display: flex;
            flex-direction: column;
            gap: 4px;
            flex: 1;
            min-width: 0;

            .permission-name-mini {
              font-size: 14px;
              font-weight: 600;
              color: $text-primary;
              overflow: hidden;
              text-overflow: ellipsis;
              white-space: nowrap;
            }

            .permission-meta {
              display: flex;
              gap: 6px;
              flex-wrap: wrap;

              .code-tag {
                max-width: 200px;
                overflow: hidden;
                text-overflow: ellipsis;
              }

              .type-tag {
                flex-shrink: 0;
              }
            }
          }
        }
      }
    }

    .permission-summary {
      padding: 16px 24px;
      background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
      border-top: 1px solid $border-lighter;

      .summary-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 14px;
        font-weight: 600;
        color: $text-primary;
        margin-bottom: 12px;

        .el-icon {
          color: $primary-color;
        }
      }

      .summary-stats {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;

        .stat-item {
          display: flex;
          align-items: center;
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
}
</style>
