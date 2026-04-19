<template>
  <div class="menu-list-page">
    <div class="page-header">
      <div class="header-left">
        <el-icon class="header-icon" :size="28"><MenuIcon /></el-icon>
        <div class="header-title">
          <h1>菜单管理</h1>
          <p>管理系统菜单和导航配置</p>
        </div>
      </div>
      <div class="header-right">
        <el-button :icon="Refresh" @click="loadData" class="icon-btn">
          刷新
        </el-button>
        <el-button type="primary" :icon="Plus" @click="handleCreate" class="primary-btn" v-permission="'menu:create'">
          新增菜单
        </el-button>
      </div>
    </div>

    <el-card class="main-card" shadow="never">
      <div class="card-content">
        <div class="search-bar">
          <div class="search-items">
            <el-input
              v-model="searchParams.keyword"
              placeholder="搜索菜单名称/编码"
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
              <el-option :value="0" label="目录" />
              <el-option :value="1" label="菜单" />
              <el-option :value="2" label="按钮" />
              <el-option :value="3" label="内嵌" />
              <el-option :value="4" label="外链" />
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
            <el-button type="primary" :icon="Search" @click="handleFilter">搜索</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </div>
        </div>

        <div class="table-wrapper">
          <el-table
            :data="tableData"
            v-loading="loading"
            stripe
            style="width: 100%"
            row-key="id"
            :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
            :indent="40"
            default-expand-all
            class="modern-table"
          >
            <el-table-column prop="name" label="菜单名称" min-width="280">
              <template #default="{ row }">
                <span class="menu-name-display">{{ row.name }}</span>
                <el-tag size="small" type="info" class="menu-code-tag">{{ row.code }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="type" label="类型" width="100">
              <template #default="{ row }">
                <el-tag :type="getMenuTypeTag(row.type)">
                  {{ getMenuTypeName(row.type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="path" label="路径" min-width="180" show-overflow-tooltip />
            <el-table-column prop="component" label="组件" min-width="180" show-overflow-tooltip />
            <el-table-column prop="sort" label="排序" width="80" />
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
                    @click="handleCreateChild(row)"
                    v-permission="'menu:create'"
                  >
                    <el-icon><Plus /></el-icon>
                    子菜单
                  </el-button>
                  <el-button
                    link
                    type="primary"
                    size="small"
                    @click="handleEdit(row)"
                    v-permission="'menu:update'"
                  >
                    <el-icon><Edit /></el-icon>
                    编辑
                  </el-button>
                  <el-button
                    link
                    type="danger"
                    size="small"
                    @click="handleDelete(row)"
                    v-permission="'menu:delete'"
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
        </div>
      </div>
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'create' ? '新增菜单' : '编辑菜单'"
      width="700px"
      :close-on-click-modal="false"
      class="menu-dialog"
    >
      <el-form ref="formRef" :model="formData" :rules="rules" label-width="100px" class="menu-form">
        <el-divider content-position="left">
          <span class="divider-title">
            <el-icon><Setting /></el-icon>
            基本信息
          </span>
        </el-divider>

        <el-form-item label="上级菜单" prop="parentId">
          <el-tree-select
            v-model="formData.parentId"
            :data="menuTree"
            :props="{ label: 'name', value: 'id' }"
            clearable
            check-strictly
            placeholder="无（顶级菜单）"
            style="width: 100%"
          />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="菜单名称" prop="name">
              <el-input v-model="formData.name" placeholder="请输入菜单名称" maxlength="50" show-word-limit clearable>
                <template #prefix>
                  <el-icon><MenuIcon /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="菜单编码" prop="code">
              <el-input 
                v-model="formData.code" 
                :disabled="dialogType === 'edit'" 
                placeholder="请输入菜单编码（英文）"
                maxlength="50"
                show-word-limit
                clearable
              >
                <template #prefix>
                  <el-icon><Key /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="菜单类型" prop="type">
          <el-radio-group v-model="formData.type" class="type-radio-group">
            <el-radio :value="0" class="type-radio">
              <span class="radio-content">
                <el-icon :color="'#409eff'"><Folder /></el-icon>
                目录
              </span>
            </el-radio>
            <el-radio :value="1" class="type-radio">
              <span class="radio-content">
                <el-icon :color="'#67c23a'"><Document /></el-icon>
                菜单
              </span>
            </el-radio>
            <el-radio :value="2" class="type-radio">
              <span class="radio-content">
                <el-icon :color="'#e6a23c'"><Operation /></el-icon>
                按钮
              </span>
            </el-radio>
            <el-radio :value="3" class="type-radio">
              <span class="radio-content">
                <el-icon :color="'#909399'"><Monitor /></el-icon>
                内嵌
              </span>
            </el-radio>
            <el-radio :value="4" class="type-radio">
              <span class="radio-content">
                <el-icon :color="'#f56c6c'"><Link /></el-icon>
                外链
              </span>
            </el-radio>
          </el-radio-group>
        </el-form-item>

        <el-divider content-position="left">
          <span class="divider-title">
            <el-icon><Document /></el-icon>
            详细信息
          </span>
        </el-divider>

        <el-form-item label="访问路径" prop="path" v-if="formData.type !== 2">
          <el-input v-model="formData.path" :placeholder="getPathPlaceholder()" maxlength="255" show-word-limit clearable>
            <template #prefix>
              <el-icon><Position /></el-icon>
            </template>
          </el-input>
          <div class="form-tip" v-if="formData.type === 4">
            <el-icon><InfoFilled /></el-icon>
            <span>外链需包含http://或https://</span>
          </div>
        </el-form-item>

        <el-form-item label="组件路径" prop="component" v-if="formData.type === 1">
          <el-input v-model="formData.component" placeholder="如: views/users/UserListPage" maxlength="255" show-word-limit clearable>
            <template #prefix>
              <el-icon><Files /></el-icon>
            </template>
          </el-input>
          <div class="form-tip">
            <el-icon><InfoFilled /></el-icon>
            <span>组件相对views目录的路径，省略.vue扩展名</span>
          </div>
        </el-form-item>

        <el-form-item label="菜单图标" prop="icon" v-if="formData.type !== 2">
          <div class="icon-picker-wrapper">
            <el-input 
              v-model="formData.icon" 
              placeholder="选择或输入图标名称"
              readonly
              @click="iconPickerVisible = true"
              clearable
            >
              <template #prefix>
                <el-icon v-if="formData.icon">
                  <component :is="formData.icon" />
                </el-icon>
                <el-icon v-else><Star /></el-icon>
              </template>
            </el-input>
          </div>
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="排序" prop="sort">
              <el-input-number 
                v-model="formData.sort" 
                :min="0" 
                :max="9999"
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
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <div class="footer-left">
            <el-tag v-if="dialogType === 'edit'" type="info" size="small">
              <el-icon><InfoFilled /></el-icon>
              菜单编码不可修改
            </el-tag>
          </div>
          <div class="footer-right">
            <el-button @click="dialogVisible = false" class="cancel-btn">
              <el-icon><Close /></el-icon>
              取消
            </el-button>
            <el-button type="primary" :loading="submitLoading" @click="handleSubmit" class="submit-btn">
              <el-icon><Check /></el-icon>
              {{ dialogType === 'create' ? '创建菜单' : '保存修改' }}
            </el-button>
          </div>
        </div>
      </template>
    </el-dialog>

    <el-dialog
      v-model="iconPickerVisible"
      title="选择图标"
      width="700px"
      class="icon-picker-dialog"
    >
      <div class="icon-search">
        <el-input
          v-model="iconSearch"
          placeholder="搜索图标"
          :prefix-icon="Search"
          clearable
        />
      </div>
      <div class="icon-grid">
        <div
          v-for="icon in filteredIcons"
          :key="icon"
          class="icon-item"
          :class="{ active: formData.icon === icon }"
          @click="selectIcon(icon)"
        >
          <el-icon><component :is="icon" /></el-icon>
          <span>{{ icon }}</span>
        </div>
      </div>
      <template #footer>
        <el-button @click="iconPickerVisible = false">取消</el-button>
        <el-button type="primary" @click="iconPickerVisible = false">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { menuService } from '@/services'
import type { Menu, MenuCreateRequest } from '@/types'
import { 
  Plus, 
  Download, 
  Refresh, 
  Search, 
  InfoFilled, 
  HomeFilled,
  User, 
  Setting, 
  Lock, 
  Key, 
  Menu as MenuIcon, 
  Grid, 
  List, 
  Document, 
  Folder, 
  FolderOpened, 
  Files, 
  Edit, 
  Delete, 
  Check, 
  Close, 
  CircleCheck, 
  CircleClose, 
  CirclePlus, 
  ArrowUp, 
  ArrowDown, 
  ArrowLeft, 
  ArrowRight, 
  Top, 
  Bottom, 
  Back, 
  Right, 
  Sort, 
  Filter, 
  ZoomIn, 
  ZoomOut, 
  FullScreen, 
  Cpu, 
  Monitor, 
  Iphone, 
  Phone, 
  Message, 
  ChatDotRound, 
  Bell, 
  BellFilled, 
  Notebook, 
  Tickets, 
  Coin, 
  Wallet, 
  CreditCard, 
  Goods, 
  ShoppingCart, 
  ShoppingBag, 
  TakeawayBox, 
  Food, 
  Dish, 
  Van, 
  Location, 
  Position, 
  OfficeBuilding, 
  House, 
  School, 
  Platform, 
  DataLine, 
  DataBoard, 
  PieChart, 
  TrendCharts, 
  Histogram, 
  Odometer, 
  Reading, 
  Management, 
  UserFilled, 
  Switch, 
  Operation, 
  Tools, 
  ScaleToOriginal, 
  Aim, 
  Select, 
  Scissor, 
  Brush, 
  MagicStick, 
  Lollipop, 
  IceTea, 
  Coffee, 
  ColdDrink, 
  Bowl, 
  Cherry, 
  Apple, 
  Pear, 
  Orange, 
  Grape, 
  Watermelon, 
  Moon, 
  Sunny, 
  Cloudy, 
  PartlyCloudy, 
  MostlyCloudy, 
  Drizzling, 
  Umbrella, 
  Lightning, 
  Sunrise, 
  Sunset, 
  MoonNight, 
  Compass, 
  MapLocation, 
  Place, 
  LocationFilled, 
  Guide, 
  Connection, 
  Present, 
  Box, 
  Briefcase, 
  Suitcase, 
  DocumentCopy, 
  DocumentAdd, 
  DocumentRemove, 
  DocumentDelete, 
  DocumentChecked, 
  FolderAdd, 
  FolderRemove, 
  FolderDelete, 
  FolderChecked, 
  Avatar, 
  Unlock, 
  Link,
  Star
} from '@element-plus/icons-vue'
import { exportToCSV, flattenTree } from '@/utils/export'
import { formatDate } from '@/utils/date'

const iconList = [
  'HomeFilled', 'User', 'Setting', 'Lock', 'Key', 'Menu', 'Grid', 'List', 'Document', 'Folder',
  'FolderOpened', 'Files', 'Edit', 'Delete', 'Check', 'Close',
  'Refresh', 'Download', 'Link', 'Picture', 'VideoCamera', 'Microphone',
  'Calendar', 'Clock', 'Timer', 'AlarmClock', 'Warning', 'CircleCheck',
  'CircleClose', 'CirclePlus', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight',
  'Top', 'Bottom', 'Back', 'Right', 'Sort', 'Filter', 'Search', 'ZoomIn', 'ZoomOut', 'FullScreen',
  'Cpu', 'Monitor', 'Iphone', 'Phone', 'Message', 'ChatDotRound', 'Bell',
  'Notebook', 'Tickets', 'Coin', 'Wallet', 'CreditCard', 'Goods', 'ShoppingCart',
  'ShoppingBag', 'DataLine', 'DataBoard', 'PieChart', 'TrendCharts', 'Histogram', 'Odometer',
  'Reading', 'Management', 'UserFilled', 'Switch', 'Operation', 'Tools',
  'Platform', 'OfficeBuilding', 'House', 'School', 'Van', 'Location', 'Position',
  'Connection', 'Present', 'Box', 'Briefcase', 'Suitcase', 'DocumentCopy', 'DocumentAdd', 'Reading',
  'Avatar', 'Unlock', 'FolderAdd', 'FolderRemove', 'FolderChecked', 'DocumentChecked', 'Star',
  'PartlyCloudy', 'MostlyCloudy', 'Drizzling', 'Moon', 'Sunny', 'Cloudy', 'Umbrella', 'Lightning',
  'Sunrise', 'Sunset', 'MoonNight', 'Compass', 'MapLocation', 'Place',
  'LocationFilled', 'Guide', 'MagicStick', 'Lollipop', 'IceTea', 'Coffee', 'ColdDrink',
  'Bowl', 'Cherry', 'Apple', 'Pear', 'Orange', 'Grape', 'Watermelon',
  'Food', 'Dish', 'TakeawayBox', 'ScaleToOriginal', 'Aim', 'Select', 'Scissor', 'Brush'
]

const loading = ref(false)
const tableData = ref<Menu[]>([])
const originalMenuTree = ref<Menu[]>([])
const menuTree = ref<Menu[]>([])
const iconPickerVisible = ref(false)
const iconSearch = ref('')

const searchParams = reactive({
  keyword: '',
  type: undefined as number | undefined,
  status: undefined as number | undefined
})

const filteredIcons = computed(() => {
  if (!iconSearch.value) return iconList
  return iconList.filter(icon => 
    icon.toLowerCase().includes(iconSearch.value.toLowerCase())
  )
})

const dialogVisible = ref(false)
const dialogType = ref<'create' | 'edit'>('create')
const formRef = ref<FormInstance>()
const formData = reactive({
  id: null as number | null,
  parentId: null as number | null,
  name: '',
  code: '',
  type: 1,
  path: '',
  component: '',
  icon: '',
  sort: 0,
  status: 1
})

const rules: FormRules = {
  parentId: [],
  name: [
    { required: true, message: '请输入菜单名称', trigger: 'blur' },
    { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入菜单编码', trigger: 'blur' },
    { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' },
    { pattern: /^[a-zA-Z][a-zA-Z0-9_]*$/, message: '只能包含字母、数字和下划线，且以字母开头', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择菜单类型', trigger: 'change' }
  ],
  path: [
    { 
      validator: (rule, value, callback) => {
        if (formData.type !== 2 && !value) {
          callback(new Error('请输入访问路径'))
        } else if (formData.type === 4 && value && !/^(https?:\/\/)/.test(value)) {
          callback(new Error('外链地址必须以http://或https://开头'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  component: [
    {
      validator: (rule, value, callback) => {
        if (formData.type === 1 && !value) {
          callback(new Error('请输入组件路径'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const submitLoading = ref(false)

const getMenuTypeName = (type: number): string => {
  const typeMap: Record<number, string> = {
    0: '目录',
    1: '菜单',
    2: '按钮',
    3: '内嵌',
    4: '外链'
  }
  return typeMap[type] || '未知'
}

const getMenuTypeTag = (type: number): 'success' | 'warning' | 'info' | 'danger' | 'primary' => {
  const tagMap: Record<number, 'success' | 'warning' | 'info' | 'danger' | 'primary'> = {
    0: 'info',
    1: 'primary',
    2: 'success',
    3: 'warning',
    4: 'danger'
  }
  return tagMap[type] || 'primary'
}

const getPathPlaceholder = (): string => {
  const placeholderMap: Record<number, string> = {
    0: '请输入目录路径，如: /system',
    1: '请输入菜单路由路径，如: /system/users',
    3: '请输入内嵌页面地址',
    4: '请输入外链地址'
  }
  return placeholderMap[formData.type] || '请输入访问路径'
}

const loadData = async () => {
  loading.value = true
  try {
    menuTree.value = await menuService.getMenuTree()
    originalMenuTree.value = JSON.parse(JSON.stringify(menuTree.value))
    tableData.value = menuTree.value
  } finally {
    loading.value = false
  }
}

const filterMenuTree = (menus: Menu[], filters: any): Menu[] => {
  const result: Menu[] = []
  
  for (const menu of menus) {
    let matches = true
    
    if (filters.keyword) {
      const keyword = filters.keyword.toLowerCase()
      if (!menu.name.toLowerCase().includes(keyword) && !menu.code.toLowerCase().includes(keyword)) {
        matches = false
      }
    }
    
    if (filters.type !== undefined && menu.type !== filters.type) {
      matches = false
    }
    
    if (filters.status !== undefined && menu.status !== filters.status) {
      matches = false
    }
    
    let filteredChildren: Menu[] = []
    if (menu.children && menu.children.length > 0) {
      filteredChildren = filterMenuTree(menu.children, filters)
    }
    
    if (matches || filteredChildren.length > 0) {
      result.push({
        ...menu,
        children: filteredChildren.length > 0 ? filteredChildren : undefined
      })
    }
  }
  
  return result
}

const handleFilter = () => {
  if (!searchParams.keyword && searchParams.type === undefined && searchParams.status === undefined) {
    tableData.value = originalMenuTree.value
    return
  }
  
  const filtered = filterMenuTree(originalMenuTree.value, searchParams)
  tableData.value = filtered
}

const resetSearch = () => {
  searchParams.keyword = ''
  searchParams.type = undefined
  searchParams.status = undefined
  tableData.value = originalMenuTree.value
}

const handleCreate = () => {
  dialogType.value = 'create'
  resetForm()
  dialogVisible.value = true
}

const handleCreateChild = (row: Menu) => {
  dialogType.value = 'create'
  resetForm()
  formData.parentId = row.id
  dialogVisible.value = true
}

const handleEdit = (row: Menu) => {
  dialogType.value = 'edit'
  Object.assign(formData, {
    id: row.id,
    parentId: row.parentId || null,
    name: row.name,
    code: row.code,
    type: row.type,
    path: row.path || '',
    component: row.component || '',
    icon: row.icon || '',
    sort: row.sort,
    status: row.status
  })
  dialogVisible.value = true
}

const resetForm = () => {
  Object.assign(formData, {
    id: null,
    parentId: null,
    name: '',
    code: '',
    type: 1,
    path: '',
    component: '',
    icon: '',
    sort: 0,
    status: 1
  })
  formRef.value?.clearValidate()
}

const selectIcon = (icon: string) => {
  formData.icon = icon
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitLoading.value = true
      try {
        const data = {
          ...formData,
          parentId: formData.parentId ?? undefined
        }
        if (dialogType.value === 'create') {
          await menuService.createMenu(data as any)
          ElMessage.success('创建成功')
        } else {
          await menuService.updateMenu(formData.id!, data as any)
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

const handleDelete = async (row: Menu) => {
  try {
    await ElMessageBox.confirm('确定要删除该菜单吗? 删除后将无法恢复！', '提示', {
      type: 'warning',
      confirmButtonText: '确定删除',
      cancelButtonText: '取消'
    })
    await menuService.deleteMenu(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch {
  }
}

const handleExport = () => {
  const headers = [
    { key: 'id', title: 'ID' },
    { key: 'name', title: '菜单名称' },
    { key: 'code', title: '菜单编码' },
    { key: 'type', title: '类型' },
    { key: 'path', title: '路径' },
    { key: 'component', title: '组件' },
    { key: 'icon', title: '图标' },
    { key: 'sort', title: '排序' },
    { key: 'status', title: '状态' }
  ]
  
  const flatData = flattenTree(tableData.value)
  const exportData = flatData.map((item: any) => ({
    ...item,
    type: getMenuTypeName(item.type),
    status: item.status === 1 ? '启用' : '禁用'
  }))
  
  const filename = `菜单数据_${formatDate(new Date(), 'YYYY-MM-DD')}`
  exportToCSV(exportData, filename, headers)
  ElMessage.success('导出成功')
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';

.menu-list-page {
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

    .table-wrapper {
      margin-bottom: 20px;
    }

    .pagination-wrapper {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  }

  .cell-name {
    display: flex;
    align-items: center;
    gap: 12px;

    .menu-icon-mini,
    .menu-icon-mini-empty {
      width: 40px;
      height: 40px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      
      .el-icon {
        font-size: 20px;
        color: white;
      }
    }

    .menu-icon-mini {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    .menu-icon-mini-empty {
      background: linear-gradient(135deg, #e0e0e0 0%, #c0c0c0 100%);
    }

    .menu-info-mini {
      display: flex;
      flex-direction: column;
      gap: 4px;

      .menu-name-mini {
        font-size: 14px;
        font-weight: 500;
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
        background: #10b981;
      }
      
      &.inactive {
        background: #ef4444;
      }
    }
  }

  .action-buttons {
    display: flex;
    gap: 4px;
  }

  .menu-dialog {
    :deep(.el-dialog__body) {
      padding: 24px;
    }
  }

  .menu-form {
    .divider-title {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 14px;
      font-weight: 600;
      color: $text-primary;
    }

    .form-tip {
      display: flex;
      align-items: center;
      gap: 4px;
      font-size: 12px;
      color: $text-secondary;
      margin-top: 4px;
    }

    .icon-picker-wrapper {
      width: 100%;
    }

    .type-radio-group,
    .status-radio-group {
      display: flex;
      gap: 16px;

      .type-radio,
      .status-radio {
        .radio-content {
          display: flex;
          align-items: center;
          gap: 6px;
        }
      }
    }
  }

  .dialog-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .footer-left {
      display: flex;
      gap: 8px;
    }

    .footer-right {
      display: flex;
      gap: 12px;

      .cancel-btn,
      .submit-btn {
        border-radius: $border-radius-lg;
        padding: 8px 20px;
      }
    }
  }

  .icon-picker-dialog {
    .icon-search {
      margin-bottom: 16px;
    }
    
    .icon-grid {
      display: grid;
      grid-template-columns: repeat(8, 1fr);
      gap: 8px;
      max-height: 400px;
      overflow-y: auto;
      
      .icon-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 4px;
        padding: 12px 8px;
        border: 1px solid $border-lighter;
        border-radius: $border-radius;
        cursor: pointer;
        transition: all 0.2s;
        
        &:hover {
          border-color: $primary-color;
          background-color: rgba(64, 158, 255, 0.1);
        }
        
        &.active {
          border-color: $primary-color;
          background-color: rgba(64, 158, 255, 0.2);
        }
        
        .el-icon {
          font-size: 24px;
          color: $text-primary;
        }
        
        span {
          font-size: 10px;
          color: $text-secondary;
          text-align: center;
          word-break: break-all;
        }
      }
    }
  }
}
</style>
