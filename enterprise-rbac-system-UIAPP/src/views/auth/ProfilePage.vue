<template>
  <div class="profile-page">
    <div class="page-header">
      <div class="header-left">
        <el-icon class="header-icon" :size="28"><User /></el-icon>
        <div class="header-title">
          <h1>个人中心</h1>
          <p>管理您的个人信息和账户设置</p>
        </div>
      </div>
      <div class="header-right">
        <el-button :icon="Refresh" @click="loadUserInfo" class="icon-btn">刷新</el-button>
      </div>
    </div>

    <el-card class="main-card" shadow="never">
      <div class="card-content">
        <el-row :gutter="40">
          <el-col :span="8">
            <div class="avatar-section">
              <div class="avatar-wrapper">
                <el-avatar :size="140" :icon="UserFilled" class="user-avatar" />
              </div>
              <div class="avatar-actions">
                <el-button type="primary" :icon="Upload" size="default" class="primary-btn">
                  更换头像
                </el-button>
              </div>
            </div>
          </el-col>
          <el-col :span="16">
            <el-form ref="formRef" :model="formData" :rules="rules" label-width="100px" class="profile-form">
              <el-divider content-position="left">
                <span class="divider-title">
                  <el-icon><Document /></el-icon>
                  基本信息
                </span>
              </el-divider>
              
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="用户名">
                    <el-input v-model="formData.username" disabled :prefix-icon="User" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="昵称" prop="nickname">
                    <el-input v-model="formData.nickname" :prefix-icon="Edit" placeholder="请输入昵称" />
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="邮箱" prop="email">
                    <el-input v-model="formData.email" :prefix-icon="Message" placeholder="请输入邮箱" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="手机号" prop="phone">
                    <el-input v-model="formData.phone" :prefix-icon="Phone" placeholder="请输入手机号" />
                  </el-form-item>
                </el-col>
              </el-row>

              <el-divider content-position="left">
                <span class="divider-title">
                  <el-icon><Clock /></el-icon>
                  登录信息
                </span>
              </el-divider>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="最后登录时间">
                    <el-input v-model="formData.lastLoginTime" disabled :prefix-icon="Clock" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="最后登录IP">
                    <el-input v-model="formData.lastLoginIp" disabled :prefix-icon="Location" />
                  </el-form-item>
                </el-col>
              </el-row>

              <div class="form-actions">
                <div class="actions-left">
                  <el-tag type="info" size="small">
                    <el-icon><InfoFilled /></el-icon>
                    建议填写完整的个人信息
                  </el-tag>
                </div>
                <div class="actions-right">
                  <el-button :icon="RefreshLeft" @click="loadUserInfo">重置</el-button>
                  <el-button type="primary" :icon="Check" :loading="loading" @click="handleSubmit" class="primary-btn">
                    保存修改
                  </el-button>
                  <el-button :icon="Lock" @click="showPasswordDialog = true">
                    修改密码
                  </el-button>
                </div>
              </div>
            </el-form>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <el-dialog v-model="showPasswordDialog" :title="dialogTitle" width="500px" :close-on-click-modal="false" class="password-dialog">
      <el-form ref="passwordFormRef" :model="passwordForm" :rules="passwordRules" label-width="100px">
        <el-divider content-position="left">
          <span class="divider-title">
            <el-icon><Lock /></el-icon>
            密码安全
          </span>
        </el-divider>
        <el-form-item label="原密码" prop="oldPassword">
          <el-input v-model="passwordForm.oldPassword" type="password" show-password :prefix-icon="Lock" placeholder="请输入原密码" />
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input v-model="passwordForm.newPassword" type="password" show-password :prefix-icon="Key" placeholder="请输入新密码（至少6位）" />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="passwordForm.confirmPassword" type="password" show-password :prefix-icon="CircleCheck" placeholder="请再次输入新密码" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <div class="footer-left">
            <el-tag type="warning" size="small">
              <el-icon><WarningFilled /></el-icon>
              修改密码后需要重新登录
            </el-tag>
          </div>
          <div class="footer-right">
            <el-button @click="showPasswordDialog = false">取消</el-button>
            <el-button type="primary" :loading="passwordLoading" @click="handlePasswordSubmit" class="primary-btn">
              确定修改
            </el-button>
          </div>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { useUserStore } from '@/store'
import { authService } from '@/services'
import { 
  UserFilled, 
  User, 
  Refresh, 
  Upload, 
  Document, 
  Edit, 
  Message, 
  Phone, 
  Clock, 
  Location, 
  RefreshLeft, 
  Check, 
  Lock, 
  Key, 
  CircleCheck, 
  InfoFilled, 
  WarningFilled 
} from '@element-plus/icons-vue'
import type { UserInfo, ChangePasswordRequest } from '@/types'

const userStore = useUserStore()

const formRef = ref<FormInstance>()
const loading = ref(false)
const showPasswordDialog = ref(false)
const passwordFormRef = ref<FormInstance>()
const passwordLoading = ref(false)

const dialogTitle = computed(() => '修改密码')

const formData = reactive({
  username: '',
  nickname: '',
  email: '',
  phone: '',
  lastLoginTime: '',
  lastLoginIp: ''
})

const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const rules: FormRules = {
  nickname: [{ required: true, message: '请输入昵称', trigger: 'blur' }],
  email: [
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ]
}

const validateConfirmPassword = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== passwordForm.newPassword) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const passwordRules: FormRules = {
  oldPassword: [{ required: true, message: '请输入原密码', trigger: 'blur' }],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少 6 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const loadUserInfo = () => {
  const user = userStore.userInfo
  if (user) {
    Object.assign(formData, {
      username: user.username,
      nickname: user.nickname,
      email: user.email || '',
      phone: user.phone || '',
      lastLoginTime: user.lastLoginTime || '-',
      lastLoginIp: user.lastLoginIp || '-'
    })
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        ElMessage.success('保存成功')
        await userStore.fetchUserInfo()
        loadUserInfo()
      } finally {
        loading.value = false
      }
    }
  })
}

const handlePasswordSubmit = async () => {
  if (!passwordFormRef.value) return
  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      passwordLoading.value = true
      try {
        await authService.changePassword({
          oldPassword: passwordForm.oldPassword,
          newPassword: passwordForm.newPassword
        } as ChangePasswordRequest)
        ElMessage.success('密码修改成功')
        showPasswordDialog.value = false
        passwordForm.oldPassword = ''
        passwordForm.newPassword = ''
        passwordForm.confirmPassword = ''
      } finally {
        passwordLoading.value = false
      }
    }
  })
}

onMounted(() => {
  loadUserInfo()
})
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';

.profile-page {
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

    .avatar-section {
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 40px 20px;
      background: linear-gradient(180deg, rgba(64, 158, 255, 0.05) 0%, rgba(103, 194, 58, 0.03) 100%);
      border-radius: $border-radius-xl;
      border: 1px dashed $border-lighter;

      .avatar-wrapper {
        margin-bottom: 20px;

        .user-avatar {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
        }
      }

      .avatar-actions {
        .primary-btn {
          border-radius: $border-radius-lg;
          padding: 10px 24px;
        }
      }
    }

    .profile-form {
      padding: 0 20px;

      .divider-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 14px;
        font-weight: 600;
        color: $text-regular;
      }

      :deep(.el-divider__text) {
        background-color: #fff;
        padding: 0 16px;
      }

      :deep(.el-divider--horizontal) {
        margin: 24px 0;
      }

      .form-actions {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 32px;
        padding-top: 24px;
        border-top: 1px solid $border-lighter;

        .actions-left {
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .actions-right {
          display: flex;
          gap: 12px;

          .primary-btn {
            border-radius: $border-radius-lg;
            padding: 10px 24px;
          }
        }
      }
    }
  }

  :deep(.el-button) {
    border-radius: $border-radius-lg;
    font-weight: 500;
  }

  :deep(.el-input__wrapper) {
    border-radius: $border-radius-lg;
    box-shadow: 0 0 0 1px $border-color inset;
    transition: all 0.3s;

    &:hover {
      box-shadow: 0 0 0 1px $primary-color inset;
    }

    &.is-focus {
      box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2) inset;
    }

    &.is-disabled {
      background: $background-color;
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
        font-size: 18px;
      }
    }

    .el-dialog__body {
      padding: 24px;

      .divider-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 14px;
        font-weight: 600;
        color: $text-regular;
      }

      :deep(.el-divider__text) {
        background-color: #fff;
        padding: 0 16px;
      }
    }

    .el-dialog__footer {
      padding: 16px 24px;
      background: #f8fafc;
      border-top: 1px solid $border-lighter;

      .dialog-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;

        .footer-left {
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .footer-right {
          display: flex;
          gap: 12px;

          .primary-btn {
            border-radius: $border-radius-lg;
            padding: 10px 24px;
          }
        }
      }
    }
  }
}
</style>
