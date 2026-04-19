<template>
  <el-container class="main-layout">
    <el-aside :width="isCollapse ? '64px' : '220px'" class="aside">
      <div class="logo">
        <span v-if="!isCollapse">RBAC管理系统</span>
        <span v-else>RBAC</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapse"
        :unique-opened="true"
        router
        class="menu"
      >
        <template v-for="item in menuItems" :key="item.path">
          <el-sub-menu v-if="item.children && item.children.length > 0" :index="item.path">
            <template #title>
              <el-icon v-if="item.meta?.icon">
                <component :is="item.meta.icon" />
              </el-icon>
              <span>{{ item.meta?.title || item.name }}</span>
            </template>
            <template v-for="child in item.children" :key="child.path">
              <el-sub-menu v-if="child.children && child.children.length > 0" :index="child.path">
                <template #title>
                  <el-icon v-if="child.meta?.icon">
                    <component :is="child.meta.icon" />
                  </el-icon>
                  <span>{{ child.meta?.title || child.name }}</span>
                </template>
                <el-menu-item
                  v-for="grandChild in child.children"
                  :key="grandChild.path"
                  :index="grandChild.path"
                >
                  {{ grandChild.meta?.title || grandChild.name }}
                </el-menu-item>
              </el-sub-menu>
              <el-menu-item v-else :index="child.path">
                <el-icon v-if="child.meta?.icon">
                  <component :is="child.meta.icon" />
                </el-icon>
                {{ child.meta?.title || child.name }}
              </el-menu-item>
            </template>
          </el-sub-menu>
          <el-menu-item v-else :index="item.path">
            <el-icon v-if="item.meta?.icon">
              <component :is="item.meta.icon" />
            </el-icon>
            <span>{{ item.meta?.title || item.name }}</span>
          </el-menu-item>
        </template>
      </el-menu>
    </el-aside>

    <el-container class="main-container">
      <el-header class="header">
        <div class="header-left">
          <div class="collapse-btn" @click="toggleCollapse">
            <el-icon v-if="!isCollapse">
              <Fold />
            </el-icon>
            <el-icon v-else>
              <Expand />
            </el-icon>
          </div>
          <el-breadcrumb separator="/" class="simple-breadcrumb">
            <el-breadcrumb-item v-for="item in breadcrumbs" :key="item.path">
              {{ item.title }}
            </el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <div class="user-info">
              <el-avatar :size="32" :icon="UserFilled" />
              <span class="username">{{ userStore.userInfo?.nickname || 'Admin' }}</span>
              <el-icon class="arrow-icon">
                <ArrowDown />
              </el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>
                  个人中心
                </el-dropdown-item>
                <el-dropdown-item command="logout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-tabs
        v-model="tabsStore.activeTab"
        type="card"
        closable
        class="tabs"
        @tab-remove="handleTabRemove"
        @tab-click="handleTabClick"
      >
        <el-tab-pane
          v-for="tab in tabsStore.tabs"
          :key="tab.path"
          :name="tab.path"
          :closable="tab.path !== '/dashboard'"
        >
          <template #label>
            <div
              class="tab-label"
              @contextmenu.prevent="showContextMenu($event, tab)"
            >
              {{ tab.title }}
            </div>
          </template>
        </el-tab-pane>
      </el-tabs>

      <div v-show="contextMenu.visible" :style="contextMenu.style" class="context-menu">
        <div class="context-menu-item" @click="handleCloseOther">
          <el-icon><Minus /></el-icon>
          关闭其他
        </div>
        <div class="context-menu-item" @click="handleCloseLeft">
          <el-icon><DArrowLeft /></el-icon>
          关闭左侧
        </div>
        <div class="context-menu-item" @click="handleCloseRight">
          <el-icon><DArrowRight /></el-icon>
          关闭右侧
        </div>
        <div class="context-menu-divider"></div>
        <div class="context-menu-item" @click="handleCloseAll">
          <el-icon><Close /></el-icon>
          关闭全部
        </div>
      </div>

      <el-main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore, useTabsStore } from '@/store'
import { ElMessageBox, ElMessage } from 'element-plus'
import {
  Fold,
  Expand,
  UserFilled,
  ArrowDown,
  User,
  SwitchButton,
  Close,
  DArrowLeft,
  DArrowRight,
  Minus
} from '@element-plus/icons-vue'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import { sessionTimeout } from '@/utils/sessionTimeout'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const tabsStore = useTabsStore()

const isCollapse = ref(false)
const contextMenu = ref({
  visible: false,
  style: {
    left: '0px',
    top: '0px'
  },
  currentTab: null as any
})

const hideContextMenu = () => {
  contextMenu.value.visible = false
}

const showContextMenu = (e: MouseEvent, tab: any) => {
  contextMenu.value.style.left = e.clientX + 'px'
  contextMenu.value.style.top = e.clientY + 'px'
  contextMenu.value.currentTab = tab
  contextMenu.value.visible = true
}

const handleCloseOther = () => {
  if (contextMenu.value.currentTab) {
    tabsStore.closeOtherTabs(contextMenu.value.currentTab.path)
    router.push(contextMenu.value.currentTab.path)
  }
  hideContextMenu()
}

const handleCloseLeft = () => {
  if (contextMenu.value.currentTab) {
    tabsStore.closeLeftTabs(contextMenu.value.currentTab.path)
    router.push(contextMenu.value.currentTab.path)
  }
  hideContextMenu()
}

const handleCloseRight = () => {
  if (contextMenu.value.currentTab) {
    tabsStore.closeRightTabs(contextMenu.value.currentTab.path)
    router.push(contextMenu.value.currentTab.path)
  }
  hideContextMenu()
}

const handleCloseAll = () => {
  tabsStore.closeAllTabs()
  router.push('/dashboard')
  hideContextMenu()
}

document.addEventListener('click', hideContextMenu)

const activeMenu = computed(() => route.path)

const getIconComponent = (iconName: string | undefined) => {
  if (!iconName) return null
  
  const iconMap: Record<string, any> = {
    setting: 'Setting',
    user: 'User',
    team: 'UserFilled',
    key: 'Lock',
    menu: 'Menu',
    apartment: 'OfficeBuilding',
    usergroup: 'User',
    monitor: 'Monitor',
    online: 'Connection',
    log: 'Document',
    audit: 'Document',
    config: 'Tools',
    parameter: 'Tools',
    book: 'Reading',
    'user-center': 'User',
    info: 'InfoFilled',
    lock: 'Lock'
  }
  
  const mappedName = iconMap[iconName] || iconName
  const iconComp = (ElementPlusIconsVue as any)[mappedName]
  return iconComp || null
}

const menuItems = computed(() => {
  if (!userStore.menus || userStore.menus.length === 0) {
    return []
  }
  
  const ensureAbsolutePath = (path: string): string => {
    if (!path) return ''
    if (path.startsWith('/')) return path
    return '/' + path
  }
  
  const transformMenu = (menu: any): any => {
    const result: any = {
      path: ensureAbsolutePath(menu.path || ''),
      name: menu.name,
      meta: {
        title: menu.name,
        icon: getIconComponent(menu.icon),
        permission: menu.code
      }
    }
    
    if (menu.children && menu.children.length > 0) {
      result.children = menu.children.map(transformMenu)
    }
    
    return result
  }
  
  const transformed = userStore.menus.map(transformMenu)
  return transformed
})

const breadcrumbs = computed(() => {
  const matched = route.matched.filter((r) => r.meta?.title)
  return matched.map((r) => ({
    path: r.path,
    title: r.meta?.title as string
  }))
})

const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
}

const handleTabRemove = (path: string) => {
  const newPath = tabsStore.removeTab(path)
  if (newPath) {
    router.push(newPath)
  } else if (tabsStore.tabs.length === 0) {
    router.push('/dashboard')
  }
}

const handleTabClick = (tab: any) => {
  router.push(tab.props.name)
}

const handleCommand = async (command: string) => {
  if (command === 'logout') {
    try {
      await ElMessageBox.confirm('确定要退出登录吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
      userStore.logout()
      router.push('/login')
      ElMessage.success('已退出登录')
    } catch {
    }
  } else if (command === 'profile') {
    router.push('/profile')
  }
}

onMounted(() => {
  if (userStore.isLoggedIn) {
    sessionTimeout.init()
  }
})

onUnmounted(() => {
  sessionTimeout.destroy()
})
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';

.main-layout {
  height: 100%;
}

.aside {
  background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow-x: hidden;
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.1);

  .logo {
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 18px;
    font-weight: 700;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(255, 255, 255, 0.05);
    letter-spacing: 1px;
    overflow: hidden;
    white-space: nowrap;
    
    span {
      transition: opacity 0.2s ease;
    }
  }

  .menu {
    border: none;
    background: transparent;
  }

  :deep(.el-menu-item),
  :deep(.el-sub-menu__title) {
    color: rgba(255, 255, 255, 0.7);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    margin: 4px 12px;
    border-radius: 8px;

    &:hover {
      color: #fff;
      background: rgba(255, 255, 255, 0.1);
    }
  }

  :deep(.el-menu-item.is-active) {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #fff;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  }

  :deep(.el-sub-menu .el-menu) {
    background: rgba(0, 0, 0, 0.2);
  }

  :deep(.el-menu--collapse) {
    .el-menu-item,
    .el-sub-menu__title {
      margin: 4px;
    }
  }
}

.main-container {
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
}

.header {
  height: 64px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);

  .header-left {
    display: flex;
    align-items: center;
    gap: 24px;

    .collapse-btn {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 40px;
      height: 40px;
      cursor: pointer;
      color: $text-secondary;
      border-radius: 8px;
      transition: all 0.3s;
      background: rgba(102, 126, 234, 0.05);
      border: 1px solid rgba(102, 126, 234, 0.1);

      .el-icon {
        font-size: 20px;
      }

      &:hover {
        color: $primary-color;
        background: rgba(102, 126, 234, 0.15);
        border-color: rgba(102, 126, 234, 0.3);
        transform: scale(1.05);
      }

      &:active {
        transform: scale(0.95);
      }
    }

    .simple-breadcrumb {
      :deep(.el-breadcrumb__item) {
        .el-breadcrumb__inner {
          color: #303133;
          font-size: 14px;
          font-weight: 500;
          transition: color 0.2s;

          &:hover {
            color: #667eea;
          }

          &.is-link {
            cursor: pointer;

            &:hover {
              color: #667eea;
            }
          }
        }

        &:last-child {
          .el-breadcrumb__inner {
            color: #303133;
            font-weight: 500;
          }
        }

        .el-breadcrumb__separator {
          color: #909399;
          margin: 0 8px;
          font-weight: 500;
        }
      }
    }
  }

  .header-right {
    .user-info {
      display: flex;
      align-items: center;
      gap: 12px;
      cursor: pointer;
      padding: 6px 12px;
      border-radius: 10px;
      transition: all 0.3s;

      &:hover {
        background: rgba(102, 126, 234, 0.1);
      }

      .username {
        color: $text-primary;
        font-weight: 500;
      }

      .arrow-icon {
        font-size: 12px;
        color: $text-secondary;
      }
    }
  }
}

.tabs {
  background: #fff;
  margin: 0;
  padding: 0 24px;

  :deep(.el-tabs__header) {
    margin: 0;
    padding: 12px 0 0;
  }

  :deep(.el-tabs__nav-wrap::after) {
    height: 1px;
    background: $border-lighter;
  }

  :deep(.el-tabs__active-bar) {
    height: 3px;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    border-radius: 3px 3px 0 0;
  }

  :deep(.el-tabs__item) {
    border: none;
    background: transparent;
    margin-right: 8px;
    border-radius: 8px 8px 0 0;
    height: 40px;
    line-height: 40px;
    padding: 0 20px;
    font-weight: 500;
    font-size: 14px;
    color: $text-secondary;
    transition: all 0.2s ease;

    &:hover {
      color: $primary-color;
      background: rgba(102, 126, 234, 0.06);
    }

    &.is-active {
      color: $primary-color;
      font-weight: 600;
    }

    .el-tabs__close {
      margin-left: 6px;
      border-radius: 4px;
      width: 16px;
      height: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s;
      opacity: 0.5;

      &:hover {
        background: rgba(245, 108, 108, 0.12);
        color: $danger-color;
        opacity: 1;
      }
    }
  }

  .tab-label {
    user-select: none;
  }
}

.context-menu {
  position: fixed;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  padding: 8px 0;
  min-width: 150px;

  .context-menu-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 16px;
    cursor: pointer;
    transition: all 0.2s;
    color: $text-primary;
    font-size: 14px;

    &:hover {
      background: rgba(102, 126, 234, 0.08);
      color: $primary-color;
    }

    .el-icon {
      font-size: 16px;
    }
  }

  .context-menu-divider {
    height: 1px;
    background: $border-lighter;
    margin: 6px 0;
  }
}

.main-content {
  flex: 1;
  padding: 24px;
  overflow: auto;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
