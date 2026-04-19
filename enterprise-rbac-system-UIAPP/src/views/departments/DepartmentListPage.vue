<template>
  <div class="department-list-page">
    <div class="page-header">
      <div class="header-left">
        <el-icon class="header-icon" :size="28"><OfficeBuilding /></el-icon>
        <div class="header-title">
          <h1>部门管理</h1>
          <p>管理组织架构和部门信息</p>
        </div>
      </div>
      <div class="header-right">
        <el-button :icon="Refresh" @click="loadData" class="icon-btn">
          刷新
        </el-button>
        <el-button type="primary" :icon="Plus" @click="handleCreate" class="primary-btn" v-permission="'department:create'">
          新增部门
        </el-button>
      </div>
    </div>

    <el-card class="main-card" shadow="never">
      <div class="card-content">
        <div class="search-bar">
          <div class="search-items">
            <el-input
              v-model="searchParams.keyword"
              placeholder="搜索部门名称/编码"
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
            <el-table-column prop="name" label="部门名称" min-width="280">
              <template #default="{ row }">
                <span class="dept-name-display">{{ row.name }}</span>
                <el-tag size="small" type="info" class="dept-code-tag">{{ row.code }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="leaderId" label="负责人ID" width="120" />
            <el-table-column prop="contactPhone" label="联系电话" width="150" />
            <el-table-column prop="address" label="地址" min-width="180" show-overflow-tooltip />
            <el-table-column prop="description" label="描述" min-width="180" show-overflow-tooltip />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <div class="status-cell">
                  <span class="status-dot" :class="row.status === 1 ? 'active' : 'inactive'"></span>
                  <span>{{ row.status === 1 ? '启用' : '禁用' }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="220" fixed="right">
              <template #default="{ row }">
                <div class="action-buttons">
                  <el-button
                    link
                    type="primary"
                    size="small"
                    @click="handleCreateChild(row)"
                    v-permission="'department:create'"
                  >
                    <el-icon><Plus /></el-icon>
                    子部门
                  </el-button>
                  <el-button
                    link
                    type="primary"
                    size="small"
                    @click="handleEdit(row)"
                    v-permission="'department:update'"
                  >
                    <el-icon><Edit /></el-icon>
                    编辑
                  </el-button>
                  <el-button
                    link
                    type="danger"
                    size="small"
                    @click="handleDelete(row)"
                    v-permission="'department:delete'"
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
      :title="dialogType === 'create' ? '新增部门' : '编辑部门'"
      width="700px"
      :close-on-click-modal="false"
      class="department-dialog"
    >
      <el-form ref="formRef" :model="formData" :rules="rules" label-width="100px" class="department-form">
        <el-divider content-position="left">
          <span class="divider-title">
            <el-icon><Setting /></el-icon>
            基本信息
          </span>
        </el-divider>

        <el-form-item label="上级部门" prop="parentId">
          <el-tree-select
            v-model="formData.parentId"
            :data="departmentTree"
            :props="{ label: 'name', value: 'id' }"
            clearable
            check-strictly
            placeholder="无（顶级部门）"
            style="width: 100%"
          />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="部门名称" prop="name">
              <el-input v-model="formData.name" placeholder="请输入部门名称" maxlength="50" show-word-limit clearable>
                <template #prefix>
                  <el-icon><OfficeBuilding /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="部门编码" prop="code">
              <el-input 
                v-model="formData.code" 
                :disabled="dialogType === 'edit'" 
                placeholder="请输入部门编码（英文）"
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

        <el-divider content-position="left">
          <span class="divider-title">
            <el-icon><Document /></el-icon>
            详细信息
          </span>
        </el-divider>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="负责人ID" prop="leaderId">
              <el-input-number 
                v-model="formData.leaderId" 
                :min="0" 
                :max="999999"
                placeholder="请输入负责人ID"
                style="width: 100%"
                controls-position="right"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="contactPhone">
              <el-input 
                v-model="formData.contactPhone" 
                placeholder="请输入联系电话"
                maxlength="20"
                show-word-limit
                clearable
              >
                <template #prefix>
                  <el-icon><Phone /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="地址" prop="address">
          <el-input 
            v-model="formData.address" 
            placeholder="请输入部门地址"
            maxlength="255"
            show-word-limit
            clearable
          >
            <template #prefix>
              <el-icon><Location /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item label="描述" prop="description">
          <el-input 
            v-model="formData.description" 
            type="textarea" 
            :rows="4"
            placeholder="请输入部门描述信息"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>

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
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <div class="footer-left">
            <el-tag v-if="dialogType === 'edit'" type="info" size="small">
              <el-icon><InfoFilled /></el-icon>
              部门编码不可修改
            </el-tag>
          </div>
          <div class="footer-right">
            <el-button @click="dialogVisible = false" class="cancel-btn">
              <el-icon><Close /></el-icon>
              取消
            </el-button>
            <el-button type="primary" :loading="submitLoading" @click="handleSubmit" class="submit-btn">
              <el-icon><Check /></el-icon>
              {{ dialogType === 'create' ? '创建部门' : '保存修改' }}
            </el-button>
          </div>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { departmentService } from '@/services'
import type { Department, DepartmentCreateRequest } from '@/types'
import { 
  Plus, 
  Download, 
  Refresh, 
  Search,
  InfoFilled,
  OfficeBuilding,
  Key,
  Setting,
  Document,
  Phone,
  Location,
  Edit,
  Delete,
  Check,
  Close,
  CircleCheck,
  CircleClose
} from '@element-plus/icons-vue'
import { exportToCSV, flattenTree } from '@/utils/export'
import { formatDate } from '@/utils/date'

const loading = ref(false)
const tableData = ref<Department[]>([])
const originalDepartmentTree = ref<Department[]>([])
const departmentTree = ref<Department[]>([])

const searchParams = reactive({
  keyword: '',
  status: undefined as number | undefined
})

const dialogVisible = ref(false)
const dialogType = ref<'create' | 'edit'>('create')
const formRef = ref<FormInstance>()
const formData = reactive({
  id: null as number | null,
  parentId: null as number | null,
  name: '',
  code: '',
  leaderId: null as number | null,
  contactPhone: '',
  address: '',
  description: '',
  status: 1
})

const rules: FormRules = {
  parentId: [],
  name: [
    { required: true, message: '请输入部门名称', trigger: 'blur' },
    { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入部门编码', trigger: 'blur' },
    { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' },
    { pattern: /^[a-zA-Z][a-zA-Z0-9_]*$/, message: '只能包含字母、数字和下划线，且以字母开头', trigger: 'blur' }
  ]
}

const submitLoading = ref(false)

const loadData = async () => {
  loading.value = true
  try {
    departmentTree.value = await departmentService.getDepartmentTree()
    originalDepartmentTree.value = JSON.parse(JSON.stringify(departmentTree.value))
    tableData.value = departmentTree.value
  } finally {
    loading.value = false
  }
}

const filterDepartmentTree = (departments: Department[], filters: any): Department[] => {
  const result: Department[] = []
  
  for (const dept of departments) {
    let matches = true
    
    if (filters.keyword) {
      const keyword = filters.keyword.toLowerCase()
      if (!dept.name.toLowerCase().includes(keyword) && !dept.code.toLowerCase().includes(keyword)) {
        matches = false
      }
    }
    
    if (filters.status !== undefined && dept.status !== filters.status) {
      matches = false
    }
    
    let filteredChildren: Department[] = []
    if (dept.children && dept.children.length > 0) {
      filteredChildren = filterDepartmentTree(dept.children, filters)
    }
    
    if (matches || filteredChildren.length > 0) {
      result.push({
        ...dept,
        children: filteredChildren.length > 0 ? filteredChildren : undefined
      })
    }
  }
  
  return result
}

const handleFilter = () => {
  if (!searchParams.keyword && searchParams.status === undefined) {
    tableData.value = originalDepartmentTree.value
    return
  }
  
  const filtered = filterDepartmentTree(originalDepartmentTree.value, searchParams)
  tableData.value = filtered
}

const resetSearch = () => {
  searchParams.keyword = ''
  searchParams.status = undefined
  tableData.value = originalDepartmentTree.value
}

const handleCreate = () => {
  dialogType.value = 'create'
  resetForm()
  dialogVisible.value = true
}

const handleCreateChild = (row: Department) => {
  dialogType.value = 'create'
  resetForm()
  formData.parentId = row.id
  dialogVisible.value = true
}

const handleEdit = (row: Department) => {
  dialogType.value = 'edit'
  Object.assign(formData, {
    id: row.id,
    parentId: row.parentId || null,
    name: row.name,
    code: row.code,
    leaderId: row.leaderId || null,
    contactPhone: row.contactPhone || '',
    address: row.address || '',
    description: row.description || '',
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
    leaderId: null,
    contactPhone: '',
    address: '',
    description: '',
    status: 1
  })
  formRef.value?.clearValidate()
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
          await departmentService.createDepartment(data as any)
          ElMessage.success('创建成功')
        } else {
          await departmentService.updateDepartment(formData.id!, data as any)
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

const handleDelete = async (row: Department) => {
  try {
    await ElMessageBox.confirm('确定要删除该部门吗? 删除后将无法恢复！', '提示', {
      type: 'warning',
      confirmButtonText: '确定删除',
      cancelButtonText: '取消'
    })
    await departmentService.deleteDepartment(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch {
  }
}

const handleExport = () => {
  const headers = [
    { key: 'id', title: 'ID' },
    { key: 'name', title: '部门名称' },
    { key: 'code', title: '部门编码' },
    { key: 'leaderId', title: '负责人ID' },
    { key: 'contactPhone', title: '联系电话' },
    { key: 'address', title: '地址' },
    { key: 'description', title: '描述' },
    { key: 'status', title: '状态' }
  ]
  
  const flatData = flattenTree(tableData.value)
  const exportData = flatData.map((item: any) => ({
    ...item,
    status: item.status === 1 ? '启用' : '禁用'
  }))
  
  const filename = `部门数据_${formatDate(new Date(), 'YYYY-MM-DD')}`
  exportToCSV(exportData, filename, headers)
  ElMessage.success('导出成功')
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';

.department-list-page {
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

    .dept-icon-mini {
      width: 40px;
      height: 40px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      
      .el-icon {
        font-size: 20px;
        color: white;
      }
    }

    .dept-info-mini {
      display: flex;
      flex-direction: column;
      gap: 4px;

      .dept-name-mini {
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

  .department-dialog {
    :deep(.el-dialog__body) {
      padding: 24px;
    }
  }

  .department-form {
    .divider-title {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 14px;
      font-weight: 600;
      color: $text-primary;
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
}
</style>
