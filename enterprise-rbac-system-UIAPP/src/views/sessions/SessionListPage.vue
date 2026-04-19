<template>
  <div class="session-list-page">
    <div class="page-header">
      <div class="header-left">
        <el-icon class="header-icon" :size="28"><Connection /></el-icon>
        <div class="header-title">
          <h1>会话管理</h1>
          <p>管理用户登录会话和在线状态</p>
        </div>
      </div>
      <div class="header-right">
        <el-button :icon="Refresh" @click="() => { loadData(); loadExpiredCount(); }" class="icon-btn">刷新</el-button>
        <el-button :icon="DeleteIcon" @click="handleCleanExpired" class="icon-btn" type="warning" v-permission="'user_session:delete'">
          清理过期
          <el-tag v-if="expiredCount && expiredCount.total_to_clean > 0" type="danger" size="small" style="margin-left: 8px;">
            {{ expiredCount.total_to_clean }}
          </el-tag>
        </el-button>
      </div>
    </div>

    <el-alert
      v-if="expiredCount && expiredCount.total_to_clean > 0"
      type="warning"
      :closable="false"
      style="margin-bottom: 16px;"
      show-icon
    >
      <template #title>
        当前有
        <el-tag type="danger" size="small">{{ expiredCount.expired_count }}</el-tag>
        个已过期会话和
        <el-tag type="info" size="small">{{ expiredCount.expired_status_count }}</el-tag>
        个已失效会话，合计
        <strong>{{ expiredCount.total_to_clean }}</strong>
        个会话需要清理
      </template>
    </el-alert>

    <el-card class="main-card" shadow="never">
      <div class="card-content">
        <div class="search-bar">
          <div class="search-items">
            <el-input
              v-model="searchParams.keyword"
              placeholder="搜索用户ID/IP地址"
              :prefix-icon="Search"
              clearable
              class="search-input"
            />
            <el-select
              v-model="searchParams.device_type"
              placeholder="设备类型"
              clearable
              class="search-select"
            >
              <el-option value="desktop" label="桌面端" />
              <el-option value="mobile" label="移动端" />
              <el-option value="tablet" label="平板端" />
              <el-option value="web" label="网页端" />
              <el-option value="unknown" label="未知" />
            </el-select>
            <el-select
              v-model="searchParams.status"
              placeholder="状态"
              clearable
              class="search-select"
            >
              <el-option :value="1" label="在线" />
              <el-option :value="0" label="已失效" />
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
            <el-button type="warning" :icon="SwitchButton" @click="handleBatchKick" v-permission="'user_session:update'">
              批量强制下线
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
            <el-table-column prop="userId" label="用户ID" width="100" />
            <el-table-column prop="username" label="用户名" width="120">
              <template #default="{ row }">
                <span>{{ row.username || '-' }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="nickname" label="昵称" width="120">
              <template #default="{ row }">
                <span>{{ row.nickname || '-' }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="sessionId" label="会话ID" min-width="200" show-overflow-tooltip />
            <el-table-column prop="deviceType" label="设备类型" width="120">
              <template #default="{ row }">
                <el-tag :type="getDeviceTypeTagType(row.deviceType)" size="small">
                  {{ getDeviceTypeLabel(row.deviceType) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="osInfo" label="操作系统" width="140">
              <template #default="{ row }">
                {{ row.osInfo || '-' }}
              </template>
            </el-table-column>
            <el-table-column prop="browserInfo" label="浏览器" width="140">
              <template #default="{ row }">
                {{ row.browserInfo || '-' }}
              </template>
            </el-table-column>
            <el-table-column prop="ipAddress" label="IP地址" width="140" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <div class="status-cell">
                  <span class="status-dot" :class="row.status === 1 ? 'active' : 'inactive'"></span>
                  <span>{{ row.status === 1 ? '在线' : '已失效' }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="loginTime" label="登录时间" width="180" />
            <el-table-column prop="lastActiveTime" label="最后活跃" width="180" />
            <el-table-column prop="expireTime" label="过期时间" width="180" />
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <div class="table-actions">
                  <el-button
                    type="primary"
                    link
                    :icon="View"
                    @click="handleView(row)"
                    size="small"
                  >
                    查看
                  </el-button>
                  <el-button
                    type="warning"
                    link
                    :icon="SwitchButton"
                    @click="handleKick(row)"
                    size="small"
                    v-permission="'user_session:update'"
                    :disabled="row.status !== 1"
                  >
                    强制下线
                  </el-button>
                  <el-button
                    type="danger"
                    link
                    :icon="Delete"
                    @click="handleDelete(row)"
                    size="small"
                    v-permission="'user_session:delete'"
                  >
                    删除
                  </el-button>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <div class="pagination-wrapper">
          <el-pagination
            v-model:current-page="pagination.page"
            v-model:page-size="pagination.pageSize"
            :page-sizes="[10, 20, 50, 100]"
            :total="pagination.total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>
    </el-card>

    <el-dialog
      v-model="viewDialogVisible"
      title="会话详情"
      width="600px"
      :close-on-click-modal="false"
    >
      <div class="session-detail" v-if="currentSession">
        <el-descriptions :column="1" border>
            <el-descriptions-item label="会话ID">
              {{ currentSession.sessionId }}
            </el-descriptions-item>
            <el-descriptions-item label="用户名">
              {{ currentSession.username || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="昵称">
              {{ currentSession.nickname || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="用户ID">
              {{ currentSession.userId }}
            </el-descriptions-item>
            <el-descriptions-item label="设备类型">
              <el-tag :type="getDeviceTypeTagType(currentSession.deviceType)" size="small">
                {{ getDeviceTypeLabel(currentSession.deviceType) }}
              </el-tag>
            </el-descriptions-item>
          <el-descriptions-item label="设备信息">
            {{ currentSession.deviceInfo || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="操作系统">
            {{ currentSession.osInfo || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="浏览器">
            {{ currentSession.browserInfo || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="IP地址">
            {{ currentSession.ipAddress || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="登录时间">
            {{ currentSession.loginTime }}
          </el-descriptions-item>
          <el-descriptions-item label="最后活跃时间">
            {{ currentSession.lastActiveTime }}
          </el-descriptions-item>
          <el-descriptions-item label="过期时间">
            {{ currentSession.expireTime }}
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="currentSession.status === 1 ? 'success' : 'info'" size="small">
              {{ currentSession.status === 1 ? '在线' : '已失效' }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <span class="footer-tip">查看用户会话的详细信息</span>
          <div class="footer-actions">
            <el-button @click="viewDialogVisible = false">关闭</el-button>
          </div>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import {
  Refresh,
  Search,
  Select,
  SwitchButton,
  Delete,
  View,
  Connection,
  Delete as DeleteIcon
} from '@element-plus/icons-vue'
import { sessionService } from '@/services/session'
import { useUserStore } from '@/store/modules/user'
import type { SessionInfo, SessionListParams } from '@/types'
import '@/styles/variables.scss'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const tableData = ref<SessionInfo[]>([])
const selectedIds = ref<number[]>([])
const viewDialogVisible = ref(false)
const currentSession = ref<SessionInfo | null>(null)
const expiredCount = ref<{ expired_count: number; expired_status_count: number; total_to_clean: number } | null>(null)
const loadingExpiredCount = ref(false)

const searchParams = reactive<SessionListParams>({
  keyword: '',
  device_type: undefined,
  status: undefined,
  page: 1,
  page_size: 10
})

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

const loadData = async () => {
  loading.value = true
  try {
    const params = {
      ...searchParams,
      page: pagination.page,
      page_size: pagination.pageSize
    }
    const response = await sessionService.getSessions(params)
    tableData.value = response.items || []
    pagination.total = response.total || 0
  } catch (error) {
    ElMessage.error('加载会话列表失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const loadExpiredCount = async () => {
  loadingExpiredCount.value = true
  try {
    expiredCount.value = await sessionService.countExpiredSessions()
  } catch (error) {
    console.error('获取过期会话数量失败', error)
  } finally {
    loadingExpiredCount.value = false
  }
}

const resetSearch = () => {
  searchParams.keyword = ''
  searchParams.device_type = undefined
  searchParams.status = undefined
  pagination.page = 1
  loadData()
}

const handleSelectionChange = (selection: SessionInfo[]) => {
  selectedIds.value = selection.map(item => item.id)
}

const handleSizeChange = (size: number) => {
  pagination.pageSize = size
  pagination.page = 1
  loadData()
}

const handleCurrentChange = (page: number) => {
  pagination.page = page
  loadData()
}

const handleView = (row: SessionInfo) => {
  currentSession.value = row
  viewDialogVisible.value = true
}

const handleKick = async (row: SessionInfo) => {
  ElMessageBox.confirm(
    `确定要强制用户ID为 ${row.userId} 的会话下线吗？`,
    '强制下线确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    // 用户点击确定
    try {
      await sessionService.kickUser({ session_ids: [row.id] })
      
      // 检查是否是当前用户自己的会话被下线
      if (row.sessionId === userStore.currentSessionId) {
        ElMessage.success('您已被强制下线，请重新登录')
        userStore.logout()
        router.push({ name: 'Login' })
        return
      }
      
      ElMessage.success('强制下线成功')
      loadData()
    } catch (error) {
      console.error('强制下线失败:', error)
      ElMessage.error('强制下线失败')
    }
  }).catch(() => {
    // 用户点击取消或关闭，不做任何处理
  })
}

const handleBatchKick = async () => {
  ElMessageBox.confirm(
    `确定要强制选中的 ${selectedIds.value.length} 个会话下线吗？`,
    '批量强制下线确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    // 用户点击确定
    try {
      
      // 检查选中的会话中是否有当前用户自己的会话
      const hasCurrentSession = tableData.value.some(
        session => selectedIds.value.includes(session.id) && session.sessionId === userStore.currentSessionId
      )
      
      await sessionService.kickUser({ session_ids: selectedIds.value })
      
      if (hasCurrentSession) {
        ElMessage.success('您已被强制下线，请重新登录')
        userStore.logout()
        router.push({ name: 'Login' })
        return
      }
      
      ElMessage.success('批量强制下线成功')
      selectedIds.value = []
      loadData()
    } catch (error) {
      console.error('批量强制下线失败:', error)
      ElMessage.error('批量强制下线失败')
    }
  }).catch(() => {
    // 用户点击取消或关闭，不做任何处理
  })
}

const handleDelete = async (row: SessionInfo) => {
  ElMessageBox.confirm(
    `确定要删除这个会话记录吗？`,
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    // 用户点击确定
    try {
      await sessionService.deleteSession(row.id)
      ElMessage.success('删除成功')
      loadData()
    } catch (error) {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }).catch(() => {
    // 用户点击取消或关闭，不做任何处理
  })
}

const handleCleanExpired = async () => {
  // 先获取过期会话数量
  await loadExpiredCount()
  
  if (!expiredCount.value || expiredCount.value.total_to_clean === 0) {
    ElMessage.info('当前没有需要清理的过期会话')
    return
  }
  
  const { expired_count, expired_status_count, total_to_clean } = expiredCount.value
  
  ElMessageBox.confirm(
    `确定要清理所有过期的会话吗？\n\n本次将清理：\n• 已过期会话：${expired_count} 个\n• 已失效会话：${expired_status_count} 个\n\n合计：${total_to_clean} 个会话`,
    '清理过期会话确认',
    {
      confirmButtonText: '确定清理',
      cancelButtonText: '取消',
      type: 'warning',
      dangerouslyUseHTMLString: true
    }
  ).then(async () => {
    // 用户点击确定
    try {
      const result = await sessionService.cleanExpiredSessions()
      ElMessage.success({
        message: `清理成功！\n已过期：${result.expired_count} 个\n已失效：${result.expired_status_count} 个\n合计：${result.total_cleaned} 个`,
        duration: 4000
      })
      expiredCount.value = null
      loadData()
    } catch (error) {
      console.error('清理过期会话失败:', error)
      ElMessage.error('清理过期会话失败')
    }
  }).catch(() => {
    // 用户点击取消或关闭，不做任何处理
  })
}

const getDeviceTypeLabel = (deviceType?: string) => {
  const labels: Record<string, string> = {
    desktop: '桌面端',
    mobile: '移动端',
    tablet: '平板端',
    web: '网页端',
    unknown: '未知'
  }
  return labels[deviceType || 'unknown'] || '未知'
}

const getDeviceTypeTagType = (deviceType?: string) => {
  const types: Record<string, any> = {
    desktop: 'primary',
    mobile: 'success',
    tablet: 'warning',
    web: 'primary',
    unknown: 'info'
  }
  return types[deviceType || 'unknown'] || 'info'
}

onMounted(() => {
  loadData()
  loadExpiredCount()
})
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';

.session-list-page {
  min-height: 100%;
  padding: 24px;
  background: $background-page;
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
      background: rgba(64, 158, 255, 0.1);
      padding: 12px;
      border-radius: $border-radius-lg;
    }

    .header-title {
      h1 {
        font-size: 24px;
        font-weight: 600;
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
      padding: 8px 16px;
    }

    .primary-btn {
      border-radius: $border-radius-lg;
      padding: 8px 20px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border: none;

      &:hover {
        opacity: 0.9;
      }
    }
  }
}

.main-card {
  border-radius: $border-radius-xl;
  border: 1px solid $border-lighter;

  .card-content {
    padding: 24px;
  }
}

.search-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 16px;
  background: $background-color;
  border-radius: $border-radius-lg;

  .search-items {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;

    .search-input {
      width: 240px;
    }

    .search-select {
      width: 160px;
    }
  }

  .search-actions {
    display: flex;
    gap: 8px;
  }
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding: 12px 16px;
  background: rgba(64, 158, 255, 0.05);
  border-radius: $border-radius-lg;
  border: 1px solid rgba(64, 158, 255, 0.2);

  .selected-info {
    display: flex;
    align-items: center;
    gap: 8px;
    color: $primary-color;
    font-weight: 500;
  }

  .batch-actions {
    display: flex;
    gap: 8px;
  }
}

.table-wrapper {
  margin-bottom: 20px;
}

.modern-table {
  border-radius: $border-radius-lg;
  overflow: hidden;

  :deep(.el-table__header-wrapper) {
    th {
      background: $background-color;
      color: $text-primary;
      font-weight: 600;
    }
  }

  :deep(.el-table__row) {
    &:hover {
      background: rgba(64, 158, 255, 0.02);
    }
  }

  .cell-name {
    display: flex;
    align-items: center;
    gap: 12px;

    .user-info {
      display: flex;
      flex-direction: column;

      .username {
        font-weight: 500;
        color: $text-primary;
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
        box-shadow: 0 0 0 4px rgba(103, 194, 58, 0.2);
      }

      &.inactive {
        background: $info-color;
      }
    }
  }

  .table-actions {
    display: flex;
    gap: 4px;
  }
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
}

.session-detail {
  :deep(.el-descriptions__label) {
    background: $background-color;
    font-weight: 500;
  }
}

.dialog-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;

  .footer-tip {
    color: $text-secondary;
    font-size: 13px;
  }

  .footer-actions {
    display: flex;
    gap: 12px;
  }
}
</style>
