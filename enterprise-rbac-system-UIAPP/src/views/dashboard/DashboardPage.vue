<template>
  <div class="dashboard-page">
    <div class="page-header">
      <div class="header-left">
        <div class="welcome-text">
          <h1>欢迎回来，{{ userStore.userInfo?.nickname || 'Admin' }}！</h1>
          <p>这是您的系统概览，今天是 {{ currentDate }}</p>
        </div>
      </div>
      <div class="header-right">
        <el-button :icon="Refresh" @click="handleRefresh" class="refresh-btn" :loading="loading">
          刷新数据
        </el-button>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-card" v-for="(stat, index) in statCards" :key="index">
        <div class="stat-icon" :style="{ background: stat.gradient }">
          <el-icon :size="36"><component :is="stat.icon" /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stat.value }}</div>
          <div class="stat-label">{{ stat.label }}</div>
          <div class="stat-trend" :class="stat.trend">
            <el-icon><TrendCharts /></el-icon>
            <span>{{ stat.trendText }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="content-grid">
      <div class="welcome-card">
        <div class="card-header">
          <div class="header-title">
            <el-icon class="header-icon" :size="24"><Odometer /></el-icon>
            <span>系统概览</span>
          </div>
        </div>
        <div class="welcome-content">
          <div class="welcome-banner">
            <div class="banner-text">
              <h2>企业RBAC管理系统</h2>
              <p>基于角色的权限管理系统，提供完整的用户、角色、权限、菜单、部门管理功能</p>
            </div>
            <div class="banner-icon">
              <el-icon :size="80"><Reading /></el-icon>
            </div>
          </div>
          
          <div class="quick-actions">
            <div class="section-title">
              <el-icon><MagicStick /></el-icon>
              <span>快捷操作</span>
            </div>
            <div class="actions-grid">
              <div 
                v-for="action in quickActions" 
                :key="action.path"
                class="action-item"
                @click="$router.push(action.path)"
              >
                <div class="action-icon" :style="{ background: action.gradient }">
                  <el-icon :size="28"><component :is="action.icon" /></el-icon>
                </div>
                <div class="action-label">{{ action.label }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="info-card">
        <div class="card-header">
          <div class="header-title">
            <el-icon class="header-icon" :size="24"><User /></el-icon>
            <span>用户信息</span>
          </div>
        </div>
        <div class="info-content">
          <div class="user-avatar">
            <el-avatar :size="80" :icon="UserFilled" />
          </div>
          <div class="user-name">{{ userStore.userInfo?.nickname || 'Admin' }}</div>
          <div class="user-role">超级管理员</div>
          
          <div class="info-list">
            <div class="info-item">
              <div class="info-label">
                <el-icon><User /></el-icon>
                <span>用户名</span>
              </div>
              <div class="info-value">{{ userStore.userInfo?.username || '-' }}</div>
            </div>
            <div class="info-item">
              <div class="info-label">
                <el-icon><Message /></el-icon>
                <span>邮箱</span>
              </div>
              <div class="info-value">{{ userStore.userInfo?.email || '-' }}</div>
            </div>
            <div class="info-item">
              <div class="info-label">
                <el-icon><Clock /></el-icon>
                <span>最后登录</span>
              </div>
              <div class="info-value">{{ userStore.userInfo?.lastLoginTime || '-' }}</div>
            </div>
            <div class="info-item">
              <div class="info-label">
                <el-icon><Location /></el-icon>
                <span>登录IP</span>
              </div>
              <div class="info-value">{{ userStore.userInfo?.lastLoginIp || '-' }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="metrics-grid">
      <div class="metrics-card">
        <div class="card-header">
          <div class="header-title">
            <el-icon class="header-icon" :size="24"><DataLine /></el-icon>
            <span>实时缓存统计</span>
          </div>
          <el-button :icon="Refresh" size="small" @click="loadCacheMetrics" :loading="metricsLoading">
            刷新
          </el-button>
        </div>
        <div class="metrics-content">
          <div class="metric-item">
            <div class="metric-icon" style="background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);">
              <el-icon :size="24"><CircleCheck /></el-icon>
            </div>
            <div class="metric-info">
              <div class="metric-value">{{ cacheMetrics.hitCount }}</div>
              <div class="metric-label">缓存命中</div>
            </div>
          </div>
          <div class="metric-item">
            <div class="metric-icon" style="background: linear-gradient(135deg, #f56c6c 0%, #f78989 100%);">
              <el-icon :size="24"><CircleClose /></el-icon>
            </div>
            <div class="metric-info">
              <div class="metric-value">{{ cacheMetrics.missCount }}</div>
              <div class="metric-label">缓存未命中</div>
            </div>
          </div>
          <div class="metric-item">
            <div class="metric-icon" style="background: linear-gradient(135deg, #409eff 0%, #79bbff 100%);">
              <el-icon :size="24"><TrendCharts /></el-icon>
            </div>
            <div class="metric-info">
              <div class="metric-value">{{ cacheMetrics.totalRequests }}</div>
              <div class="metric-label">总请求数</div>
            </div>
          </div>
          <div class="metric-item">
            <div class="metric-icon" style="background: linear-gradient(135deg, #e6a23c 0%, #ebb563 100%);">
              <el-icon :size="24"><DataBoard /></el-icon>
            </div>
            <div class="metric-info">
              <div class="metric-value">{{ cacheMetrics.hitRate.toFixed(2) }}%</div>
              <div class="metric-label">命中率</div>
            </div>
          </div>
        </div>
        <div class="metrics-footer">
          <el-button size="small" type="danger" @click="handleResetCacheMetrics">
            重置统计
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted, computed, markRaw, onUnmounted } from 'vue'
import { useUserStore } from '@/store'
import { 
  User, UserFilled, Key, OfficeBuilding, Refresh, 
  TrendCharts, Odometer, Reading, MagicStick, Message, Clock, Location,
  Tickets, Document, Setting, DataLine, DataBoard, CircleCheck, CircleClose
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { dashboardService } from '@/services'

const userStore = useUserStore()
const loading = ref(false)
const metricsLoading = ref(false)

const cacheMetrics = reactive({
  hitCount: 0,
  missCount: 0,
  totalRequests: 0,
  hitRate: 0
})

let metricsInterval: number | null = null

const currentDate = computed(() => {
  const now = new Date()
  return now.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  })
})

const statCards = reactive([
  {
    label: '用户总数',
    value: 0,
    icon: markRaw(User),
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    trend: 'up',
    trendText: '实时数据'
  },
  {
    label: '角色数量',
    value: 0,
    icon: markRaw(UserFilled),
    gradient: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)',
    trend: 'up',
    trendText: '实时数据'
  },
  {
    label: '权限数量',
    value: 0,
    icon: markRaw(Key),
    gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    trend: 'stable',
    trendText: '实时数据'
  },
  {
    label: '部门数量',
    value: 0,
    icon: markRaw(OfficeBuilding),
    gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    trend: 'up',
    trendText: '实时数据'
  }
])

const quickActions = [
  { 
    label: '用户管理', 
    path: '/users', 
    icon: markRaw(User),
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  },
  { 
    label: '角色管理', 
    path: '/roles', 
    icon: markRaw(UserFilled),
    gradient: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)'
  },
  { 
    label: '权限管理', 
    path: '/permissions', 
    icon: markRaw(Key),
    gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
  },
  { 
    label: '菜单管理', 
    path: '/menus', 
    icon: markRaw(Tickets),
    gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
  },
  { 
    label: '部门管理', 
    path: '/departments', 
    icon: markRaw(OfficeBuilding),
    gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
  },
  { 
    label: '操作日志', 
    path: '/logs', 
    icon: markRaw(Document),
    gradient: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)'
  },
  { 
    label: '审计日志', 
    path: '/audit-logs', 
    icon: markRaw(DataLine),
    gradient: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)'
  },
  { 
    label: '数据字典', 
    path: '/dictionaries', 
    icon: markRaw(Tickets),
    gradient: 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)'
  },
  { 
    label: '系统设置', 
    path: '/settings', 
    icon: markRaw(Setting),
    gradient: 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)'
  }
]

const loadStats = async () => {
  try {
    loading.value = true
    const data = await dashboardService.getDashboardStats()
    statCards[0].value = data.userCount
    statCards[1].value = data.roleCount
    statCards[2].value = data.permissionCount
    statCards[3].value = data.departmentCount
  } catch (error) {
    console.error('加载统计数据失败:', error)
    ElMessage.error('加载统计数据失败')
  } finally {
    loading.value = false
  }
}

const loadCacheMetrics = async () => {
  try {
    metricsLoading.value = true
    const data = await dashboardService.getCacheMetrics()
    cacheMetrics.hitCount = data.hitCount || 0
    cacheMetrics.missCount = data.missCount || 0
    cacheMetrics.totalRequests = data.totalRequests || 0
    cacheMetrics.hitRate = data.hitRate || 0
  } catch (error) {
    console.error('加载缓存统计失败:', error)
  } finally {
    metricsLoading.value = false
  }
}

const handleResetCacheMetrics = async () => {
  try {
    await ElMessageBox.confirm('确定要重置缓存统计数据吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await dashboardService.resetCacheMetrics()
    await loadCacheMetrics()
    ElMessage.success('缓存统计已重置')
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('重置缓存统计失败:', error)
      ElMessage.error('重置缓存统计失败')
    }
  }
}

const handleRefresh = async () => {
  await Promise.all([loadStats(), loadCacheMetrics()])
  ElMessage.success('数据已刷新')
}

const startMetricsInterval = () => {
  metricsInterval = window.setInterval(() => {
    loadCacheMetrics()
  }, 30000)
}

onMounted(() => {
  loadStats()
  loadCacheMetrics()
  startMetricsInterval()
})

onUnmounted(() => {
  if (metricsInterval) {
    clearInterval(metricsInterval)
  }
})
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';

.dashboard-page {
  padding: 24px;
  background: $background-page;
  min-height: calc(100vh - 60px);

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;

    .header-left {
      .welcome-text {
        h1 {
          font-size: 28px;
          font-weight: 700;
          color: $text-primary;
          margin: 0 0 8px 0;
          background: $gradient-primary;
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        p {
          font-size: 14px;
          color: $text-secondary;
          margin: 0;
        }
      }
    }

    .header-right {
      .refresh-btn {
        border-radius: $border-radius-lg;
        padding: 10px 20px;
        transition: all $transition;

        &:hover {
          transform: translateY(-2px);
          box-shadow: $shadow-lg;
        }
      }
    }
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 24px;

    .stat-card {
      background: $background-card;
      border-radius: $border-radius-xl;
      padding: 24px;
      display: flex;
      align-items: center;
      gap: 20px;
      box-shadow: $shadow-sm;
      transition: all $transition;
      cursor: pointer;

      &:hover {
        transform: translateY(-4px);
        box-shadow: $shadow-lg;
      }

      .stat-icon {
        width: 72px;
        height: 72px;
        border-radius: $border-radius-lg;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #fff;
        flex-shrink: 0;
      }

      .stat-content {
        flex: 1;

        .stat-value {
          font-size: 32px;
          font-weight: 700;
          color: $text-primary;
          line-height: 1.2;
        }

        .stat-label {
          font-size: 14px;
          color: $text-secondary;
          margin-top: 4px;
        }

        .stat-trend {
          display: flex;
          align-items: center;
          gap: 4px;
          font-size: 12px;
          margin-top: 8px;

          &.up {
            color: $success-color;
          }

          &.down {
            color: $danger-color;
          }

          &.stable {
            color: $text-secondary;
          }
        }
      }
    }
  }

  .content-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 20px;
  }

  .welcome-card,
  .info-card {
    background: $background-card;
    border-radius: $border-radius-xl;
    box-shadow: $shadow-sm;
    overflow: hidden;
    transition: all $transition;

    &:hover {
      box-shadow: $shadow;
    }

    .card-header {
      padding: 20px 24px;
      border-bottom: 1px solid $border-lighter;

      .header-title {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 16px;
        font-weight: 600;
        color: $text-primary;

        .header-icon {
          color: $primary-color;
        }
      }
    }
  }

  .welcome-card {
    .welcome-content {
      padding: 24px;

      .welcome-banner {
        background: $gradient-primary;
        border-radius: $border-radius-lg;
        padding: 32px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 24px;

        .banner-text {
          flex: 1;

          h2 {
            color: #fff;
            font-size: 24px;
            font-weight: 700;
            margin: 0 0 8px 0;
          }

          p {
            color: rgba(255, 255, 255, 0.9);
            font-size: 14px;
            margin: 0;
            line-height: 1.6;
          }
        }

        .banner-icon {
          color: rgba(255, 255, 255, 0.3);
        }
      }

      .quick-actions {
        .section-title {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 16px;
          font-weight: 600;
          color: $text-primary;
          margin-bottom: 16px;
        }

        .actions-grid {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: 16px;

          .action-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 12px;
            padding: 20px 16px;
            border-radius: $border-radius-lg;
            background: $background-color;
            cursor: pointer;
            transition: all $transition;

            &:hover {
              transform: translateY(-4px);
              box-shadow: $shadow;
              background: #fff;
            }

            .action-icon {
              width: 56px;
              height: 56px;
              border-radius: $border-radius-lg;
              display: flex;
              align-items: center;
              justify-content: center;
              color: #fff;
            }

            .action-label {
              font-size: 14px;
              font-weight: 500;
              color: $text-regular;
            }
          }
        }
      }
    }
  }

  .info-card {
    .info-content {
      padding: 24px;
      text-align: center;

      .user-avatar {
        margin-bottom: 16px;
      }

      .user-name {
        font-size: 20px;
        font-weight: 700;
        color: $text-primary;
        margin-bottom: 4px;
      }

      .user-role {
        font-size: 14px;
        color: $text-secondary;
        margin-bottom: 24px;
      }

      .info-list {
        .info-item {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 12px 0;
          border-bottom: 1px solid $border-lighter;

          &:last-child {
            border-bottom: none;
          }

          .info-label {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 14px;
            color: $text-secondary;
          }

          .info-value {
            font-size: 14px;
            color: $text-regular;
            font-weight: 500;
          }
        }
      }
    }
  }

  .metrics-grid {
    margin-top: 20px;
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .metrics-card {
    background: $background-card;
    border-radius: $border-radius-xl;
    box-shadow: $shadow-sm;
    overflow: hidden;
    transition: all $transition;

    &:hover {
      box-shadow: $shadow;
    }

    .card-header {
      padding: 20px 24px;
      border-bottom: 1px solid $border-lighter;
      display: flex;
      justify-content: space-between;
      align-items: center;

      .header-title {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 16px;
        font-weight: 600;
        color: $text-primary;

        .header-icon {
          color: $primary-color;
        }
      }
    }

    .metrics-content {
      padding: 24px;
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 20px;
    }

    .metric-item {
      display: flex;
      align-items: center;
      gap: 16px;
      padding: 20px;
      background: $background-color;
      border-radius: $border-radius-lg;
      transition: all $transition;

      &:hover {
        transform: translateY(-2px);
        box-shadow: $shadow;
      }

      .metric-icon {
        width: 56px;
        height: 56px;
        border-radius: $border-radius-lg;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #fff;
        flex-shrink: 0;
      }

      .metric-info {
        flex: 1;
      }

      .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: $text-primary;
        margin-bottom: 4px;
      }

      .metric-label {
        font-size: 14px;
        color: $text-secondary;
      }
    }

    .metrics-footer {
      padding: 16px 24px;
      background: $background-color;
      border-top: 1px solid $border-lighter;
    }
  }
}

@media (max-width: 1400px) {
  .dashboard-page {
    .stats-grid {
      grid-template-columns: repeat(2, 1fr);
    }

    .content-grid {
      grid-template-columns: 1fr;
    }

    .metrics-card {
      .metrics-content {
        grid-template-columns: repeat(2, 1fr);
      }
    }
  }
}

@media (max-width: 768px) {
  .dashboard-page {
    padding: 16px;

    .stats-grid {
      grid-template-columns: 1fr;
    }

    .welcome-card {
      .welcome-content {
        .quick-actions {
          .actions-grid {
            grid-template-columns: repeat(2, 1fr);
          }
        }
      }
    }

    .metrics-card {
      .metrics-content {
        grid-template-columns: 1fr;
      }
    }
  }
}
</style>
