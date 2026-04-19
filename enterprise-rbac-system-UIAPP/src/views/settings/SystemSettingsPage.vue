<template>
  <div class="system-settings-page">
    <div class="page-header">
      <span class="page-title">系统设置</span>
      <el-button type="primary" @click="handleSave" :loading="loading">
        保存设置
      </el-button>
    </div>

    <el-row :gutter="20" align="top">
      <el-col :span="16">
        <el-card class="settings-card">
          <template #header>
            <div class="card-header">
              <el-icon><Setting /></el-icon>
              <span>基本设置</span>
            </div>
          </template>
          <el-form :model="basicSettings" label-width="120px" label-position="right">
            <el-form-item label="系统名称">
              <el-input v-model="basicSettings.systemName" placeholder="请输入系统名称" />
            </el-form-item>
            <el-form-item label="系统Logo">
              <el-input v-model="basicSettings.systemLogo" placeholder="请输入Logo地址" />
            </el-form-item>
            <el-form-item label="系统描述">
              <el-input v-model="basicSettings.systemDesc" type="textarea" :rows="3" placeholder="请输入系统描述" />
            </el-form-item>
            <el-form-item label="备案号">
              <el-input v-model="basicSettings.icp" placeholder="请输入备案号" />
            </el-form-item>
            <el-form-item label="版权信息">
              <el-input v-model="basicSettings.copyright" placeholder="请输入版权信息" />
            </el-form-item>
          </el-form>
        </el-card>

        <el-card class="settings-card" style="margin-top: 20px">
          <template #header>
            <div class="card-header">
              <el-icon><Lock /></el-icon>
              <span>安全设置</span>
            </div>
          </template>
          <el-form :model="securitySettings" label-width="120px" label-position="right">
            <el-form-item label="密码最小长度">
              <el-input-number v-model="securitySettings.minPasswordLength" :min="6" :max="32" />
            </el-form-item>
            <el-form-item label="会话超时(分钟)">
              <el-input-number v-model="securitySettings.sessionTimeout" :min="5" :max="1440" />
            </el-form-item>
            <el-form-item label="登录失败锁定">
              <el-switch v-model="securitySettings.loginLockEnabled" />
            </el-form-item>
            <el-form-item label="失败次数锁定">
              <el-input-number v-model="securitySettings.maxLoginAttempts" :min="3" :max="10" :disabled="!securitySettings.loginLockEnabled" />
            </el-form-item>
            <el-form-item label="锁定时间(分钟)">
              <el-input-number v-model="securitySettings.lockDuration" :min="5" :max="1440" :disabled="!securitySettings.loginLockEnabled" />
            </el-form-item>
            <el-form-item label="密码复杂度">
              <el-checkbox-group v-model="securitySettings.passwordComplexity">
                <el-checkbox value="uppercase">包含大写字母</el-checkbox>
                <el-checkbox value="lowercase">包含小写字母</el-checkbox>
                <el-checkbox value="number">包含数字</el-checkbox>
                <el-checkbox value="special">包含特殊字符</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card class="settings-card">
          <template #header>
            <div class="card-header">
              <el-icon><Document /></el-icon>
              <span>系统信息</span>
            </div>
          </template>
          <el-descriptions :column="1" border label-style="text-align: right;">
            <el-descriptions-item label="系统版本">{{ systemInfo.version }}</el-descriptions-item>
            <el-descriptions-item label="框架版本">{{ systemInfo.frameworkVersion }}</el-descriptions-item>
            <el-descriptions-item label="构建时间">{{ systemInfo.buildTime }}</el-descriptions-item>
            <el-descriptions-item label="运行环境">{{ systemInfo.environment }}</el-descriptions-item>
          </el-descriptions>
        </el-card>

        <el-card class="settings-card" style="margin-top: 20px">
          <template #header>
            <div class="card-header">
              <el-icon><DataBoard /></el-icon>
              <span>服务器信息</span>
            </div>
          </template>
          <el-descriptions :column="1" border label-style="text-align: right;">
            <el-descriptions-item label="服务器地址">{{ serverInfo.address }}</el-descriptions-item>
            <el-descriptions-item label="服务器端口">{{ serverInfo.port }}</el-descriptions-item>
            <el-descriptions-item label="运行时间">{{ serverInfo.uptime }}</el-descriptions-item>
            <el-descriptions-item label="内存使用">{{ serverInfo.memory }}</el-descriptions-item>
          </el-descriptions>
        </el-card>

        <el-card class="settings-card" style="margin-top: 20px">
          <template #header>
            <div class="card-header">
              <el-icon><Tools /></el-icon>
              <span>快捷操作</span>
            </div>
          </template>
          <div class="quick-actions">
            <el-button type="primary" class="action-button" @click="handleClearCache" :loading="loading">
              <el-icon><Delete /></el-icon>
              清除缓存
            </el-button>
            <el-button type="warning" class="action-button" @click="handleRefreshConfig" :loading="loading">
              <el-icon><Refresh /></el-icon>
              刷新配置
            </el-button>
            <el-button type="danger" class="action-button" @click="handleRestart" :loading="loading">
              <el-icon><SwitchButton /></el-icon>
              重启服务
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { reactive, onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Setting,
  Lock,
  Document,
  DataBoard,
  Tools,
  Delete,
  Refresh,
  SwitchButton
} from '@element-plus/icons-vue'
import systemConfigService from '@/services/systemConfig'
import { sessionTimeout } from '@/utils/sessionTimeout'

const loading = ref(false)

const basicSettings = reactive({
  systemName: '企业RBAC管理系统',
  systemLogo: '',
  systemDesc: '基于角色的权限管理系统',
  icp: '',
  copyright: '© 2026 All Rights Reserved'
})

const securitySettings = reactive({
  minPasswordLength: 8,
  sessionTimeout: 30,
  loginLockEnabled: true,
  maxLoginAttempts: 5,
  lockDuration: 30,
  passwordComplexity: ['uppercase', 'lowercase', 'number']
})

const systemInfo = reactive({
  version: 'v1.0.0',
  frameworkVersion: 'Vue 3.4.0',
  buildTime: '2026-04-14 10:00:00',
  environment: '开发环境'
})

const serverInfo = reactive({
  address: '127.0.0.1',
  port: '5173',
  uptime: '24小时 30分钟',
  memory: '512MB / 2GB'
})

const loadData = async () => {
  loading.value = true
  try {
    const activeConfigs = await systemConfigService.getActiveConfigs()
    
    Object.keys(basicSettings).forEach(key => {
      if (activeConfigs[key] !== undefined && activeConfigs[key] !== null) {
        (basicSettings as any)[key] = activeConfigs[key]
      }
    })

    Object.keys(securitySettings).forEach(key => {
      if (activeConfigs[key] !== undefined && activeConfigs[key] !== null) {
        const value = activeConfigs[key]
        if (key === 'loginLockEnabled') {
          (securitySettings as any)[key] = value === 'true' || value === '1' || value === true
        } else if (key === 'passwordComplexity') {
          (securitySettings as any)[key] = value ? value.split(',') : []
        } else if (['minPasswordLength', 'sessionTimeout', 'maxLoginAttempts', 'lockDuration'].includes(key)) {
          (securitySettings as any)[key] = parseInt(value, 10) || (securitySettings as any)[key]
        } else {
          (securitySettings as any)[key] = value
        }
      }
    })

    // 更新会话超时配置
    if (securitySettings.sessionTimeout) {
      sessionTimeout.setTimeout(securitySettings.sessionTimeout)
    }
  } catch (error) {
    console.error('加载配置失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSave = async () => {
  try {
    await ElMessageBox.confirm('确定要保存系统设置吗?', '提示', {
      type: 'warning'
    })
    
    loading.value = true

    const configs: Record<string, any> = {}

    Object.keys(basicSettings).forEach(key => {
      const configKey = key.replace(/([A-Z])/g, '_$1').toLowerCase()
      configs[configKey] = (basicSettings as any)[key]
    })

    Object.keys(securitySettings).forEach(key => {
      const configKey = key.replace(/([A-Z])/g, '_$1').toLowerCase()
      if (key === 'loginLockEnabled') {
        configs[configKey] = (securitySettings as any)[key] ? '1' : '0'
      } else if (key === 'passwordComplexity') {
        configs[configKey] = (securitySettings as any)[key].join(',')
      } else {
        configs[configKey] = (securitySettings as any)[key]
      }
    })

    const result = await systemConfigService.batchUpdateConfigs(configs)
    ElMessage.success('设置保存成功')
    
    // 更新会话超时配置
    sessionTimeout.setTimeout(securitySettings.sessionTimeout)
    
    await loadData()
  } catch (error: any) {
    console.error('保存设置失败:', error)
    ElMessage.error(error.message || '保存设置失败')
  } finally {
    loading.value = false
  }
}

const handleClearCache = async () => {
  try {
    await ElMessageBox.confirm('确定要清除系统缓存吗?', '提示', {
      type: 'warning'
    })
    loading.value = true
    ElMessage.info('清除缓存功能需要后端实现')
  } catch {
  } finally {
    loading.value = false
  }
}

const handleRefreshConfig = async () => {
  try {
    loading.value = true
    await systemConfigService.refreshCache()
    ElMessage.success('配置刷新成功')
    await loadData()
  } catch (error) {
    console.error('刷新配置失败:', error)
  } finally {
    loading.value = false
  }
}

const handleRestart = async () => {
  try {
    await ElMessageBox.confirm('确定要重启服务吗? 重启期间系统将无法访问。', '提示', {
      type: 'warning',
      confirmButtonText: '确定重启',
      cancelButtonText: '取消'
    })
    ElMessage.info('重启服务功能需要后端实现')
  } catch {
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';

.system-settings-page {
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
    transition: all 0.3s ease;
    
    &:hover {
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
      transform: translateY(-2px);
    }

    .el-card__header {
      background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
      border-bottom: 1px solid $border-lighter;
      padding: 16px 20px;

      .card-header {
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 600;
        color: $text-primary;
        font-size: 16px;
      }
    }

    .el-card__body {
      padding: 24px;
    }
  }

  .settings-card {
    :deep(.el-input__wrapper),
    :deep(.el-textarea__inner) {
      border-radius: $border-radius-md;
      box-shadow: 0 0 0 1px $border-color inset;
      transition: all 0.3s;

      &:hover {
        box-shadow: 0 0 0 1px $primary-color inset;
      }

      &.is-focus {
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) inset;
      }
    }

    :deep(.el-form-item__label) {
      text-align: right;
      padding-right: 16px;
      font-weight: 500;
    }
    
    :deep(.el-checkbox-group) {
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
    }
  }

  .quick-actions {
    display: flex !important;
    flex-direction: column !important;
    align-items: stretch !important;
    width: 100% !important;
    
    .action-button {
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      width: 100% !important;
      margin-bottom: 10px !important;
      margin-left: 0 !important;
      border-radius: $border-radius-md;
      font-weight: 500;
      transition: all 0.3s;
      height: 44px;
      font-size: 14px;
      padding: 0 16px !important;
      text-align: center !important;
      gap: 8px;

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
      }
    }

    .action-button + .action-button {
      margin-left: 0 !important;
    }
  }

  :deep(.el-descriptions__label) {
    text-align: right !important;
    padding-right: 16px !important;
    font-weight: 500;
  }
  
  :deep(.el-descriptions__content) {
    word-break: break-all;
  }
}

@media (max-width: 1200px) {
  .system-settings-page {
    :deep(.el-col) {
      width: 100% !important;
    }
  }
}
</style>
