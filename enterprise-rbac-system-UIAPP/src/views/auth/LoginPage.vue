<template>
  <div class="login-container">
    <div class="login-background">
      <div class="bg-shape shape-1"></div>
      <div class="bg-shape shape-2"></div>
      <div class="bg-shape shape-3"></div>
    </div>
    
    <div class="login-box">
      <div class="login-header">
        <div class="logo-icon">
          <el-icon :size="48"><Lock /></el-icon>
        </div>
        <h1 class="title">企业RBAC系统</h1>
        <p class="subtitle">专业的权限管理解决方案</p>
      </div>

      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        class="login-form"
        @keyup.enter="handleLogin"
      >
        <el-form-item prop="username">
          <div class="input-wrapper">
            <div class="input-icon">
              <el-icon><User /></el-icon>
            </div>
            <el-input
              v-model="formData.username"
              placeholder="请输入用户名"
              size="large"
              class="custom-input"
            />
          </div>
        </el-form-item>

        <el-form-item prop="password">
          <div class="input-wrapper">
            <div class="input-icon">
              <el-icon><Lock /></el-icon>
            </div>
            <el-input
              v-model="formData.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              class="custom-input"
              show-password
              @keyup.enter="handleLogin"
            />
          </div>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            class="login-btn"
            @click="handleLogin"
          >
            <template v-if="!loading">
              <el-icon><Promotion /></el-icon>
              <span>登 录</span>
            </template>
            <template v-else>
              <span>登录中...</span>
            </template>
          </el-button>
        </el-form-item>
      </el-form>

      <div class="login-footer">
        <div class="footer-divider">
          <span></span>
        </div>
        <div class="hint-box">
          <el-icon><InfoFilled /></el-icon>
          <span>默认账号: admin / 123456</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { User, Lock, Promotion, InfoFilled } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref<FormInstance>()
const loading = ref(false)

const formData = reactive({
  username: '',
  password: ''
})

const rules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 5, max: 20, message: '用户名长度在 5 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少 6 个字符', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        await userStore.login(formData.username, formData.password)
        ElMessage.success('登录成功')
        router.push('/dashboard')
      } catch (error) {
        console.error('登录失败:', error)
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';

.login-container {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;

  .login-background {
    position: absolute;
    width: 100%;
    height: 100%;
    overflow: hidden;

    .bg-shape {
      position: absolute;
      border-radius: 50%;
      opacity: 0.1;

      &.shape-1 {
        width: 600px;
        height: 600px;
        background: #fff;
        top: -200px;
        left: -200px;
      }

      &.shape-2 {
        width: 400px;
        height: 400px;
        background: #fff;
        bottom: -100px;
        right: -100px;
      }

      &.shape-3 {
        width: 300px;
        height: 300px;
        background: #fff;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
      }
    }
  }

  .login-box {
    width: 440px;
    padding: 48px 40px;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: $border-radius-xl;
    box-shadow: 0 25px 80px rgba(0, 0, 0, 0.25);
    position: relative;
    z-index: 1;
    animation: slideUp 0.5s ease;

    .login-header {
      text-align: center;
      margin-bottom: 40px;

      .logo-icon {
        width: 80px;
        height: 80px;
        margin: 0 auto 20px;
        background: $gradient-primary;
        border-radius: $border-radius-xl;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #fff;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
      }

      .title {
        font-size: 28px;
        font-weight: 700;
        color: $text-primary;
        margin-bottom: 8px;
        background: $gradient-primary;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
      }

      .subtitle {
        font-size: 14px;
        color: $text-secondary;
      }
    }

    .login-form {
      :deep(.el-form-item) {
        margin-bottom: 24px;
      }
      
      .input-wrapper {
        position: relative;
        display: flex;
        align-items: center;
        width: 100%;

        .input-icon {
          position: absolute;
          left: 16px;
          z-index: 1;
          color: $text-secondary;
        }

        .custom-input {
          width: 100%;
          
          :deep(.el-input__wrapper) {
            padding-left: 44px;
            border-radius: $border-radius-lg;
            box-shadow: 0 0 0 1px $border-color inset;
            transition: all $transition;

            &:hover {
              box-shadow: 0 0 0 1px $primary-color inset;
            }

            &.is-focus {
              box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) inset;
            }
          }
        }
      }

      .login-btn {
        width: 100%;
        height: 48px;
        border-radius: $border-radius-lg;
        font-size: 16px;
        font-weight: 600;
        background: $gradient-primary;
        border: none;
        transition: all $transition;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;

        &:hover {
          transform: translateY(-2px);
          box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }

        &:active {
          transform: translateY(0);
        }
      }
    }

    .login-footer {
      margin-top: 32px;

      .footer-divider {
        display: flex;
        align-items: center;
        margin-bottom: 24px;

        span {
          flex: 1;
          height: 1px;
          background: $border-lighter;
        }
      }

      .hint-box {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        padding: 12px 16px;
        background: $background-color;
        border-radius: $border-radius-lg;
        color: $text-secondary;
        font-size: 13px;
      }
    }
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
