<template>
  <div class="dictionary-page">
    <div class="page-header">
      <span class="page-title">数据字典</span>
      <el-button :icon="Refresh" @click="loadDictTypes">
        刷新
      </el-button>
    </div>

    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="dictionary-card">
          <template #header>
            <div class="card-header">
              <span>字典类型</span>
              <el-button type="primary" link size="small" @click="handleCreateType">
                新增类型
              </el-button>
            </div>
          </template>
          <el-tree
            :data="dictionaryTypes"
            :props="treeProps"
            node-key="id"
            :highlight-current="true"
            @node-click="handleTypeClick"
            default-expand-all
          >
            <template #default="{ node, data }">
              <div class="tree-node">
                <span>{{ node.label }}</span>
                <div class="node-actions">
                  <el-button type="primary" link size="small" @click.stop="handleEditType(data)">
                    <el-icon><Edit /></el-icon>
                  </el-button>
                  <el-button type="danger" link size="small" @click.stop="handleDeleteType(data)">
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </div>
              </div>
            </template>
          </el-tree>
        </el-card>
      </el-col>

      <el-col :span="16">
        <el-card class="item-card">
          <template #header>
            <div class="card-header">
              <span>字典数据 - {{ currentTypeName || '请选择字典类型' }}</span>
              <el-button
                type="primary"
                link
                size="small"
                :disabled="!currentTypeId"
                @click="handleCreateItem"
              >
                新增数据
              </el-button>
            </div>
          </template>

          <el-table
            v-if="currentTypeId"
            :data="itemData"
            v-loading="loading"
            border
            stripe
            row-key="id"
          >
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="label" label="标签" width="150" />
            <el-table-column prop="value" label="值" width="150" />
            <el-table-column prop="sort" label="排序" width="100" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.status === 1 ? 'success' : 'danger'">
                  {{ row.status === 1 ? '启用' : '禁用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="description" label="描述" />
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="handleEditItem(row)">
                  编辑
                </el-button>
                <el-button type="danger" link size="small" @click="handleDeleteItem(row)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <el-empty v-else description="请从左侧选择字典类型" />
        </el-card>
      </el-col>
    </el-row>

    <el-dialog v-model="typeDialogVisible" :title="typeDialogTitle" width="500px">
      <el-form :model="typeForm" :rules="typeRules" ref="typeFormRef" label-width="100px">
        <el-form-item label="类型编码" prop="code">
          <el-input v-model="typeForm.code" placeholder="请输入类型编码" :disabled="!!typeForm.id" />
        </el-form-item>
        <el-form-item label="类型名称" prop="name">
          <el-input v-model="typeForm.name" placeholder="请输入类型名称" />
        </el-form-item>
        <el-form-item label="排序" prop="sort">
          <el-input-number v-model="typeForm.sort" :min="0" style="width: 100%" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="typeForm.status">
            <el-radio :value="1">启用</el-radio>
            <el-radio :value="0">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="typeForm.description" type="textarea" :rows="3" placeholder="请输入描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="typeDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleTypeSubmit">
          确定
        </el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="itemDialogVisible" :title="itemDialogTitle" width="500px">
      <el-form :model="itemForm" :rules="itemRules" ref="itemFormRef" label-width="100px">
        <el-form-item label="标签" prop="label">
          <el-input v-model="itemForm.label" placeholder="请输入标签" />
        </el-form-item>
        <el-form-item label="值" prop="value">
          <el-input v-model="itemForm.value" placeholder="请输入值" />
        </el-form-item>
        <el-form-item label="排序" prop="sort">
          <el-input-number v-model="itemForm.sort" :min="0" style="width: 100%" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="itemForm.status">
            <el-radio :value="1">启用</el-radio>
            <el-radio :value="0">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="itemForm.description" type="textarea" :rows="3" placeholder="请输入描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="itemDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleItemSubmit">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted, computed } from 'vue'
import { Plus, Refresh, Edit, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { systemDictService } from '@/services'

const loading = ref(false)
const submitLoading = ref(false)
const typeDialogVisible = ref(false)
const itemDialogVisible = ref(false)
const typeFormRef = ref<FormInstance>()
const itemFormRef = ref<FormInstance>()
const currentTypeId = ref<number | null>(null)
const currentTypeName = ref('')

const treeProps = {
  children: 'children',
  label: 'name'
}

const dictionaryTypes = ref<any[]>([])
const itemData = ref<any[]>([])

const typeForm = reactive({
  id: null as number | null,
  code: '',
  name: '',
  sort: 0,
  status: 1,
  description: ''
})

const itemForm = reactive({
  id: null as number | null,
  dict_id: null as number | null,
  label: '',
  value: '',
  sort: 0,
  status: 1,
  description: ''
})

const typeRules: FormRules = {
  code: [{ required: true, message: '请输入类型编码', trigger: 'blur' }],
  name: [{ required: true, message: '请输入类型名称', trigger: 'blur' }]
}

const itemRules: FormRules = {
  label: [{ required: true, message: '请输入标签', trigger: 'blur' }],
  value: [{ required: true, message: '请输入值', trigger: 'blur' }]
}

const typeDialogTitle = computed(() => typeForm.id ? '编辑字典类型' : '新增字典类型')
const itemDialogTitle = computed(() => itemForm.id ? '编辑字典数据' : '新增字典数据')

const loadDictTypes = async () => {
  loading.value = true
  try {
    const data = await systemDictService.getDicts({ page: 1, pageSize: 100 })
    dictionaryTypes.value = data?.data || data?.items || data || []
  } catch (error) {
    console.error('加载字典类型失败:', error)
    ElMessage.error('加载字典类型失败')
  } finally {
    loading.value = false
  }
}

const loadDictItems = async (dictId: number) => {
  loading.value = true
  try {
    const data = await systemDictService.getDictItems(dictId)
    itemData.value = data?.data || data || []
  } catch (error) {
    console.error('加载字典项失败:', error)
    ElMessage.error('加载字典项失败')
  } finally {
    loading.value = false
  }
}

const handleTypeClick = (data: any) => {
  currentTypeId.value = data.id
  currentTypeName.value = data.name
  if (data.id) {
    loadDictItems(data.id)
  }
}

const handleCreateType = () => {
  typeForm.id = null
  typeForm.code = ''
  typeForm.name = ''
  typeForm.sort = 0
  typeForm.status = 1
  typeForm.description = ''
  typeDialogVisible.value = true
}

const handleEditType = (row: any) => {
  typeForm.id = row.id
  typeForm.code = row.code
  typeForm.name = row.name
  typeForm.sort = row.sort
  typeForm.status = row.status
  typeForm.description = row.description || ''
  typeDialogVisible.value = true
}

const handleDeleteType = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要删除该字典类型吗? 删除后相关字典项也会被删除!', '提示', {
      type: 'warning'
    })
    await systemDictService.deleteDict(row.id)
    ElMessage.success('删除成功')
    if (currentTypeId.value === row.id) {
      currentTypeId.value = null
      currentTypeName.value = ''
      itemData.value = []
    }
    loadDictTypes()
  } catch {
  }
}

const handleTypeSubmit = async () => {
  if (!typeFormRef.value) return
  await typeFormRef.value.validate(async (valid) => {
    if (valid) {
      submitLoading.value = true
      try {
        if (typeForm.id) {
          await systemDictService.updateDict(typeForm.id, {
            name: typeForm.name,
            description: typeForm.description,
            sort: typeForm.sort,
            status: typeForm.status
          })
          ElMessage.success('更新成功')
        } else {
          await systemDictService.createDict({
            code: typeForm.code,
            name: typeForm.name,
            description: typeForm.description,
            sort: typeForm.sort,
            status: typeForm.status
          })
          ElMessage.success('新增成功')
        }
        typeDialogVisible.value = false
        loadDictTypes()
      } catch (error: any) {
        console.error('提交失败:', error)
        ElMessage.error(error.message || '操作失败')
      } finally {
        submitLoading.value = false
      }
    }
  })
}

const handleCreateItem = () => {
  itemForm.id = null
  itemForm.dict_id = currentTypeId.value
  itemForm.label = ''
  itemForm.value = ''
  itemForm.sort = 0
  itemForm.status = 1
  itemForm.description = ''
  itemDialogVisible.value = true
}

const handleEditItem = (row: any) => {
  itemForm.id = row.id
  itemForm.dict_id = row.dict_id
  itemForm.label = row.label
  itemForm.value = row.value
  itemForm.sort = row.sort
  itemForm.status = row.status
  itemForm.description = row.description || ''
  itemDialogVisible.value = true
}

const handleDeleteItem = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要删除该字典数据吗?', '提示', {
      type: 'warning'
    })
    await systemDictService.deleteDictItem(row.id)
    ElMessage.success('删除成功')
    if (currentTypeId.value) {
      loadDictItems(currentTypeId.value)
    }
  } catch {
  }
}

const handleItemSubmit = async () => {
  if (!itemFormRef.value) return
  await itemFormRef.value.validate(async (valid) => {
    if (valid) {
      submitLoading.value = true
      try {
        if (itemForm.id) {
          await systemDictService.updateDictItem(itemForm.id, {
            label: itemForm.label,
            value: itemForm.value,
            description: itemForm.description,
            sort: itemForm.sort,
            status: itemForm.status
          })
          ElMessage.success('更新成功')
        } else if (itemForm.dict_id) {
          await systemDictService.createDictItem(itemForm.dict_id, {
            label: itemForm.label,
            value: itemForm.value,
            description: itemForm.description,
            sort: itemForm.sort,
            status: itemForm.status
          })
          ElMessage.success('新增成功')
        }
        itemDialogVisible.value = false
        if (currentTypeId.value) {
          loadDictItems(currentTypeId.value)
        }
      } catch (error: any) {
        console.error('提交失败:', error)
        ElMessage.error(error.message || '操作失败')
      } finally {
        submitLoading.value = false
      }
    }
  })
}

onMounted(() => {
  loadDictTypes()
})
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';

.dictionary-page {
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    padding: 20px 24px;
    background: linear-gradient(135deg, #f8fafc 0%, #fff 100%);
    border-radius: $border-radius-xl;
    border: 1px solid $border-lighter;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);

    .page-title {
      font-size: 24px;
      font-weight: 700;
      color: $text-primary;
      display: flex;
      align-items: center;
      gap: 10px;

      &::before {
        content: '';
        width: 4px;
        height: 24px;
        background: $gradient-primary;
        border-radius: 2px;
      }
    }

    :deep(.el-button) {
      border-radius: $border-radius-md;
      font-weight: 500;
      transition: all 0.3s;

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
      }

      &.el-button--primary {
        background: $gradient-primary;
        border: none;
      }
    }
  }

  :deep(.el-card) {
    border: none;
    border-radius: $border-radius-xl;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);

    .el-card__header {
      background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
      border-bottom: 1px solid $border-lighter;
      padding: 16px 20px;

      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: 600;
        color: $text-primary;
      }
    }
  }

  .dictionary-card {
    height: calc(100vh - 260px);

    :deep(.el-card__body) {
      height: calc(100% - 57px);
      overflow: auto;
      padding: 20px;
    }

    :deep(.el-tree-node__content) {
      transition: all 0.3s;
      border-radius: $border-radius-md;
      padding: 0 8px;

      &:hover {
        background: rgba(102, 126, 234, 0.1);
      }

      .tree-node {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;

        .node-actions {
          opacity: 0;
          transition: opacity 0.2s;
          display: flex;
          gap: 4px;
        }
      }

      &:hover .node-actions {
        opacity: 1;
      }
    }

    :deep(.el-tree-node.is-current > .el-tree-node__content) {
      background: $gradient-primary;
      color: #fff;

      .node-actions {
        opacity: 1;
      }
    }
  }

  .item-card {
    height: calc(100vh - 260px);

    :deep(.el-card__body) {
      height: calc(100% - 57px);
      display: flex;
      flex-direction: column;
      padding: 20px;

      .el-table {
        flex: 1;
        border-radius: $border-radius-lg;
        overflow: hidden;
      }

      .el-empty {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
      }
    }
  }

  :deep(.el-dialog) {
    border-radius: $border-radius-xl;
    overflow: hidden;

    .el-dialog__header {
      background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
      padding: 20px 24px;
      border-bottom: 1px solid $border-lighter;

      .el-dialog__title {
        font-weight: 700;
        color: $text-primary;
      }
    }

    .el-dialog__body {
      padding: 24px;
    }

    .el-dialog__footer {
      padding: 16px 24px;
      background: #f8fafc;
      border-top: 1px solid $border-lighter;
    }
  }
}
</style>
