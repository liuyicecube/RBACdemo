import { ElMessage, ElMessageBox } from 'element-plus'
import { storage } from './storage'
import router from '@/router'
import { useUserStore } from '@/store/modules/user'

const SESSION_TIMEOUT_KEY = 'sessionTimeout'
const LAST_ACTIVITY_KEY = 'lastActivity'
const DEFAULT_TIMEOUT = 30 // 默认30分钟

let timeoutTimer: number | null = null
let warningTimer: number | null = null
let isShowingWarning = false

export const sessionTimeout = {
  getTimeout(): number {
    const saved = storage.getItem(SESSION_TIMEOUT_KEY)
    return saved ? parseInt(saved, 10) : DEFAULT_TIMEOUT
  },

  setTimeout(minutes: number): void {
    storage.setItem(SESSION_TIMEOUT_KEY, minutes.toString())
    this.resetTimer()
  },

  getLastActivity(): number {
    const saved = storage.getItem(LAST_ACTIVITY_KEY)
    return saved ? parseInt(saved, 10) : Date.now()
  },

  updateLastActivity(): void {
    storage.setItem(LAST_ACTIVITY_KEY, Date.now().toString())
    this.resetTimer()
  },

  resetTimer(): void {
    this.clearTimers()

    const timeoutMs = this.getTimeout() * 60 * 1000
    const warningMs = timeoutMs - 5 * 60 * 1000 // 超时前5分钟提示

    const lastActivity = this.getLastActivity()
    const elapsed = Date.now() - lastActivity
    const remaining = timeoutMs - elapsed

    if (remaining <= 0) {
      this.logout()
      return
    }

    // 设置超时定时器
    timeoutTimer = window.setTimeout(() => {
      this.logout()
    }, remaining)

    // 设置警告定时器（如果剩余时间超过5分钟）
    if (remaining > 5 * 60 * 1000) {
      warningTimer = window.setTimeout(() => {
        this.showWarning()
      }, remaining - 5 * 60 * 1000)
    }
  },

  clearTimers(): void {
    if (timeoutTimer) {
      clearTimeout(timeoutTimer)
      timeoutTimer = null
    }
    if (warningTimer) {
      clearTimeout(warningTimer)
      warningTimer = null
    }
  },

  showWarning(): void {
    if (isShowingWarning) return

    isShowingWarning = true
    ElMessageBox.alert(
      '您的会话将在5分钟后过期，请及时保存您的工作。',
      '会话超时提醒',
      {
        confirmButtonText: '我知道了',
        type: 'warning',
        onClose: () => {
          isShowingWarning = false
        }
      }
    )
  },

  logout(): void {
    this.clearTimers()
    const userStore = useUserStore()

    ElMessage.warning('您的会话已超时，请重新登录')
    userStore.logout()

    // 跳转到登录页
    if (router.currentRoute.value.path !== '/login') {
      router.push('/login')
    }
  },

  init(): void {
    // 监听用户活动
    const activities = ['mousedown', 'mousemove', 'keydown', 'scroll', 'click']
    activities.forEach(event => {
      document.addEventListener(event, () => {
        this.updateLastActivity()
      }, true)
    })

    // 启动定时器
    this.resetTimer()
  },

  destroy(): void {
    this.clearTimers()
  }
}
