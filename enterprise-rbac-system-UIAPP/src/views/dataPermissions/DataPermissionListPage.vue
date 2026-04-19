<template>
  <div class="data-permission-page">
    <div class="page-header">
      <div class="header-left">
        <el-icon class="header-icon" :size="28"><Lock /></el-icon>
        <div class="header-title">
          <h1>数据权限规则</h1>
          <p>管理系统的数据权限规则配置</p>
        </div>
      </div>
      <div class="header-right">
        <el-button :icon="Refresh" @click="loadData" class="icon-btn">
          刷新
        </el-button>
        <el-button type="primary" :icon="Plus" @click="handleCreate" class="primary-btn" v-permission="'data_permission:create'">
          新增规则
        </el-button>
      </div>
    </div>

    <el-card class="main-card" shadow="never">
      <div class="card-content">
        <div class="search-bar">
          <div class="search-items">
            <el-input
              v-model="searchParams.keyword"
              placeholder="搜索规则名称/编码"
              :prefix-icon="Search"
              clearable
              class="search-input"
            />
            <el-select
              v-model="searchParams.ruleType"
              placeholder="规则类型"
              clearable
              class="search-select"
            >
              <el-option :value="1" label="自定义SQL" />
              <el-option :value="2" label="部门数据权限" />
              <el-option :value="3" label="用户数据权限" />
              <el-option :value="4" label="角色数据权限" />
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
            <el-button type="danger" :icon="Delete" @click="handleBatchDelete" v-permission="'data_permission:delete'">
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
            <el-table-column prop="name" label="规则名称" min-width="150">
              <template #default="{ row }">
                <div class="cell-name">
                  <el-tag size="small" type="primary">{{ row.code }}</el-tag>
                  <span>{{ row.name }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="resourceTable" label="资源表" min-width="150" />
            <el-table-column prop="ruleType" label="规则类型" width="130">
              <template #default="{ row }">
                <el-tag :type="getRuleTypeTag(row.ruleType)">
                  {{ getRuleTypeName(row.ruleType) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="ruleExpression" label="规则表达式" min-width="200" show-overflow-tooltip />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <div class="status-cell">
                  <span class="status-dot" :class="row.status === 1 ? 'active' : 'inactive'"></span>
                  <span>{{ row.status === 1 ? '启用' : '禁用' }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="280" fixed="right">
              <template #default="{ row }">
                <div class="action-buttons">
                  <el-button
                    link
                    type="primary"
                    size="small"
                    @click="handleEdit(row)"
                    v-permission="'data_permission:update'"
                  >
                    <el-icon><Edit /></el-icon>
                    编辑
                  </el-button>
                  <el-button
                    link
                    type="success"
                    size="small"
                    @click="handleTest(row)"
                    v-permission="'data_permission:view'"
                  >
                    <el-icon><Cpu /></el-icon>
                    测试
                  </el-button>
                  <el-button
                    link
                    type="danger"
                    size="small"
                    @click="handleDelete(row)"
                    v-permission="'data_permission:delete'"
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
      :title="dialogType === 'create' ? '新增数据权限规则' : '编辑数据权限规则'"
      width="700px"
      :close-on-click-modal="false"
      class="modern-dialog"
    >
      <el-form ref="formRef" :model="formData" :rules="rules" label-width="120px">
        <el-form-item label="规则名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入规则名称" />
        </el-form-item>
        <el-form-item label="规则编码" prop="code">
          <el-input v-model="formData.code" placeholder="请输入规则编码" :disabled="dialogType === 'edit'" />
        </el-form-item>
        <el-form-item label="关联权限" prop="permissionId">
          <el-select v-model="formData.permissionId" placeholder="请选择关联权限（可选）" clearable style="width: 100%">
            <el-option 
              v-for="perm in allPermissions" 
              :key="perm.id" 
              :value="perm.id" 
              :label="perm.name" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="资源表" prop="resourceTable">
          <el-input v-model="formData.resourceTable" placeholder="请输入资源表名" />
        </el-form-item>
        <el-form-item label="规则类型" prop="ruleType">
          <el-radio-group v-model="formData.ruleType">
            <el-radio :value="1">自定义SQL</el-radio>
            <el-radio :value="2">部门数据权限</el-radio>
            <el-radio :value="3">用户数据权限</el-radio>
            <el-radio :value="4">角色数据权限</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="规则表达式" prop="ruleExpression">
          <el-input
            v-model="formData.ruleExpression"
            type="textarea"
            :rows="4"
            placeholder="请输入规则表达式（SQL WHERE条件）"
          />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="2"
            placeholder="请输入描述"
          />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="formData.status">
            <el-radio :value="1">启用</el-radio>
            <el-radio :value="0">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog
      v-model="testDialogVisible"
      title="测试数据权限规则"
      width="600px"
      class="test-dialog"
    >
      <div class="test-content">
        <div class="test-info">
          <el-descriptions :column="1" border>
            <el-descriptions-item label="规则名称">{{ currentTestRule?.name }}</el-descriptions-item>
            <el-descriptions-item label="规则编码">{{ currentTestRule?.code }}</el-descriptions-item>
            <el-descriptions-item label="资源表">{{ currentTestRule?.resourceTable }}</el-descriptions-item>
            <el-descriptions-item label="规则表达式">
              <el-input
                :model-value="currentTestRule?.ruleExpression"
                type="textarea"
                :rows="3"
                readonly
              />
            </el-descriptions-item>
          </el-descriptions>
        </div>
        <div class="test-result" v-if="testResult">
          <h4>测试结果：</h4>
          <el-alert
            :title="testResult.success ? '测试成功' : '测试失败'"
            :type="testResult.success ? 'success' : 'error'"
            :closable="false"
          >
            <template #default>
              <pre v-if="testResult.data" class="result-data">{{ JSON.stringify(testResult.data, null, 2) }}</pre>
              <p v-else>{{ testResult.message }}</p>
            </template>
          </el-alert>
        </div>
      </div>
      <template #footer>
        <el-button :loading="testLoading" @click="executeTest" type="primary">
          <el-icon><Cpu /></el-icon>
          执行测试
        </el-button>
        <el-button @click="testDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { dataPermissionService, permissionService } from '@/services'
import type { 
  DataPermissionRule, 
  DataPermissionRuleCreateRequest, 
  DataPermissionRuleUpdateRequest,
  Permission
} from '@/types'
import { 
  Search, Refresh, Plus, Delete, Download, Edit, Lock,
  Select, CircleCheck, CircleClose, Cpu
} from '@element-plus/icons-vue'
import { exportToCSV } from '@/utils/export'
import { formatDate } from '@/utils/date'

const loading = ref(false)
const tableData = ref<DataPermissionRule[]>([])
const allPermissions = ref<Permission[]>([])
const selectedIds = ref<number[]>([])
const currentTestRule = ref<DataPermissionRule | null>(null)
const testResult = ref<any>(null)
const testLoading = ref(false)

const searchParams = reactive({
  keyword: '',
  ruleType: undefined as number | undefined,
  status: undefined as number | undefined
})

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

const dialogVisible = ref(false)
const testDialogVisible = ref(false)
const dialogType = ref<'create' | 'edit'>('create')
const formRef = ref<FormInstance>()
const submitLoading = ref(false)
const formData = reactive({
  id: null as number | null,
  name: '',
  code: '',
  permissionId: undefined as number | undefined,
  resourceTable: '',
  ruleType: 1,
  ruleExpression: '',
  description: '',
  status: 1
})

const rules: FormRules = {
  name: [{ required: true, message: '请输入规则名称', trigger: 'blur' }],
  code: [{ required: true, message: '请输入规则编码', trigger: 'blur' }],
  resourceTable: [{ required: true, message: '请输入资源表名', trigger: 'blur' }],
  ruleType: [{ required: true, message: '请选择规则类型', trigger: 'change' }],
  ruleExpression: [{ required: true, message: '请输入规则表达式', trigger: 'blur' }]
}

const getRuleTypeName = (type: number): string => {
  const typeMap: Record<number, string> = {
    1: '自定义SQL',
    2: '部门数据权限',
    3: '用户数据权限',
    4: '角色数据权限'
  }
  return typeMap[type] || '未知'
}

const getRuleTypeTag = (type: number): string => {
  const tagMap: Record<number, string> = {
    1: 'primary',
    2: 'success',
    3: 'warning',
    4: 'danger'
  }
  return tagMap[type] || 'info'
}

const loadData = async () => {
  loading.value = true
  try {
    const data = await dataPermissionService.getDataPermissionRules({
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

const loadAllPermissions = async () => {
  const permissions = await permissionService.getAllPermissions()
  allPermissions.value = permissions
}

const resetSearch = () => {
  searchParams.keyword = ''
  searchParams.ruleType = undefined
  searchParams.status = undefined
  pagination.page = 1
  loadData()
}

const handleCreate = async () => {
  await loadAllPermissions()
  dialogType.value = 'create'
  Object.assign(formData, {
    id: null,
    name: '',
    code: '',
    permissionId: undefined,
    resourceTable: '',
    ruleType: 1,
    ruleExpression: '',
    description: '',
    status: 1
  })
  dialogVisible.value = true
}

const handleEdit = async (row: DataPermissionRule) => {
  await loadAllPermissions()
  dialogType.value = 'edit'
  Object.assign(formData, {
    id: row.id,
    name: row.name,
    code: row.code,
    permissionId: row.permissionId,
    resourceTable: row.resourceTable,
    ruleType: row.ruleType,
    ruleExpression: row.ruleExpression,
    description: row.description || '',
    status: row.status
  })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitLoading.value = true
      try {
        if (dialogType.value === 'create') {
          await dataPermissionService.createDataPermissionRule(formData as DataPermissionRuleCreateRequest)
          ElMessage.success('创建成功')
        } else {
          await dataPermissionService.updateDataPermissionRule(formData.id!, formData as DataPermissionRuleUpdateRequest)
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

const handleDelete = async (row: DataPermissionRule) => {
  try {
    await ElMessageBox.confirm('确定要删除该数据权限规则吗?', '提示', {
      type: 'warning'
    })
    await dataPermissionService.deleteDataPermissionRule(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch {
  }
}

const handleTest = (row: DataPermissionRule) => {
  currentTestRule.value = row
  testResult.value = null
  testDialogVisible.value = true
}

const executeTest = async () => {
  if (!currentTestRule.value) return
  testLoading.value = true
  try {
    const result = await dataPermissionService.testDataPermissionRule(currentTestRule.value.id)
    testResult.value = {
      success: true,
      data: result,
      message: '测试执行成功'
    }
    ElMessage.success('测试成功')
  } catch (error: any) {
    testResult.value = {
      success: false,
      message: error.message || '测试失败'
    }
  } finally {
    testLoading.value = false
  }
}

const handleSelectionChange = (selection: DataPermissionRule[]) => {
  selectedIds.value = selection.map(item => item.id)
}

const handleBatchEnable = async () => {
  try {
    await ElMessageBox.confirm(`确定要启用选中的 ${selectedIds.value.length} 个规则吗?`, '提示', {
      type: 'success'
    })
    const promises = selectedIds.value.map(id => dataPermissionService.updateDataPermissionRuleStatus(id, 1))
    await Promise.all(promises)
    ElMessage.success('批量启用成功')
    selectedIds.value = []
    loadData()
  } catch {
  }
}

const handleBatchDisable = async () => {
  try {
    await ElMessageBox.confirm(`确定要禁用选中的 ${selectedIds.value.length} 个规则吗?`, '提示', {
      type: 'warning'
    })
    const promises = selectedIds.value.map(id => dataPermissionService.updateDataPermissionRuleStatus(id, 0))
    await Promise.all(promises)
    ElMessage.success('批量禁用成功')
    selectedIds.value = []
    loadData()
  } catch {
  }
}

const handleBatchDelete = async () => {
  try {
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedIds.value.length} 个规则吗?`, '提示', {
      type: 'warning'
    })
    const promises = selectedIds.value.map(id => dataPermissionService.deleteDataPermissionRule(id))
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
    { key: 'name', title: '规则名称' },
    { key: 'code', title: '规则编码' },
    { key: 'resourceTable', title: '资源表' },
    { key: 'ruleType', title: '规则类型' },
    { key: 'ruleExpression', title: '规则表达式' },
    { key: 'status', title: '状态' }
  ]
  
  const exportData = tableData.value.map(item => ({
    ...item,
    ruleType: getRuleTypeName(item.ruleType),
    status: item.status === 1 ? '启用' : '禁用'
  }))
  
  const filename = `数据权限规则_${formatDate(new Date(), 'YYYY-MM-DD')}`
  exportToCSV(exportData, filename, headers)
  ElMessage.success('导出成功')
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';

.data-permission-page {
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
          gap: 8px;
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
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 20px 24px;
      
      .el-dialog__title {
        color: #fff;
        font-weight: 700;
        font-size: 18px;
      }
      
      .el-dialog__headerbtn {
        .el-dialog__close {
          color: #fff;
          font-size: 20px;
        }
      }
    }

    :deep(.el-dialog__body) {
      padding: 24px;
    }

    :deep(.el-dialog__footer) {
      padding: 16px 24px;
      background: #f8fafc;
      border-top: 1px solid $border-lighter;
    }
  }

  .test-dialog {
    :deep(.el-dialog__header) {
      background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
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
        }
      }
    }

    :deep(.el-dialog__body) {
      padding: 24px;
    }

    .test-content {
      .test-info {
        margin-bottom: 20px;
      }

      .test-result {
        h4 {
          margin-bottom: 12px;
          color: $text-primary;
        }

        .result-data {
          background: #f5f7fa;
          padding: 12px;
          border-radius: $border-radius-sm;
          font-size: 12px;
          max-height: 200px;
          overflow-y: auto;
          margin-top: 12px;
        }
      }
    }

    :deep(.el-dialog__footer) {
      padding: 16px 24px;
      background: #f8fafc;
      border-top: 1px solid $border-lighter;
    }
  }
}
</style>
