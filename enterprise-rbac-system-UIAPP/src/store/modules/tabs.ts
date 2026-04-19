import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import type { RouteLocationNormalized } from 'vue-router'

const DASHBOARD_PATH = '/dashboard'
const DASHBOARD_TITLE = '仪表盘'
const TABS_STORAGE_KEY = 'enterprise_rbac_tabs'
const ACTIVE_TAB_STORAGE_KEY = 'enterprise_rbac_active_tab'

export interface TabItem {
  path: string
  name: string
  title: string
}

const loadTabsFromStorage = (): TabItem[] => {
  try {
    const stored = localStorage.getItem(TABS_STORAGE_KEY)
    if (stored) {
      const parsed = JSON.parse(stored)
      if (Array.isArray(parsed) && parsed.length > 0) {
        const hasDashboard = parsed.some((tab) => tab.path === DASHBOARD_PATH)
        if (!hasDashboard) {
          parsed.unshift({
            path: DASHBOARD_PATH,
            name: 'Dashboard',
            title: DASHBOARD_TITLE
          })
        }
        return parsed
      }
    }
  } catch (e) {
    console.error('Failed to load tabs from storage:', e)
  }
  return [
    {
      path: DASHBOARD_PATH,
      name: 'Dashboard',
      title: DASHBOARD_TITLE
    }
  ]
}

const loadActiveTabFromStorage = (): string => {
  try {
    const stored = localStorage.getItem(ACTIVE_TAB_STORAGE_KEY)
    if (stored) {
      return stored
    }
  } catch (e) {
    console.error('Failed to load active tab from storage:', e)
  }
  return DASHBOARD_PATH
}

export const useTabsStore = defineStore('tabs', () => {
  const tabs = ref<TabItem[]>(loadTabsFromStorage())
  const activeTab = ref<string>(loadActiveTabFromStorage())

  const saveTabsToStorage = (): void => {
    try {
      localStorage.setItem(TABS_STORAGE_KEY, JSON.stringify(tabs.value))
      localStorage.setItem(ACTIVE_TAB_STORAGE_KEY, activeTab.value)
    } catch (e) {
      console.error('Failed to save tabs to storage:', e)
    }
  }

  watch(
    [tabs, activeTab],
    () => {
      saveTabsToStorage()
    },
    { deep: true }
  )

  const addTab = (route: RouteLocationNormalized): void => {
    const exists = tabs.value.find((tab) => tab.path === route.path)
    if (!exists && route.name && route.path !== DASHBOARD_PATH) {
      tabs.value.push({
        path: route.path,
        name: route.name as string,
        title: (route.meta?.title as string) || route.name as string
      })
    }
    if (route.path) {
      activeTab.value = route.path
    }
  }

  const removeTab = (path: string): string | null => {
    if (path === DASHBOARD_PATH) {
      return tabs.value.length > 0 ? activeTab.value : null
    }
    const index = tabs.value.findIndex((tab) => tab.path === path)
    if (index > -1) {
      tabs.value.splice(index, 1)
      if (tabs.value.length > 0) {
        if (activeTab.value === path) {
          const newIndex = Math.min(index, tabs.value.length - 1)
          return tabs.value[newIndex].path
        }
      }
    }
    return null
  }

  const closeOtherTabs = (path: string): void => {
    const dashboardTab = tabs.value.find((tab) => tab.path === DASHBOARD_PATH)
    const currentTab = tabs.value.find((tab) => tab.path === path)
    tabs.value = []
    if (dashboardTab) {
      tabs.value.push(dashboardTab)
    }
    if (currentTab && currentTab.path !== DASHBOARD_PATH) {
      tabs.value.push(currentTab)
    }
    activeTab.value = path
  }

  const closeAllTabs = (): void => {
    const dashboardTab = tabs.value.find((tab) => tab.path === DASHBOARD_PATH)
    tabs.value = []
    if (dashboardTab) {
      tabs.value.push(dashboardTab)
    }
    activeTab.value = DASHBOARD_PATH
  }

  const closeLeftTabs = (path: string): void => {
    const index = tabs.value.findIndex((tab) => tab.path === path)
    if (index > 0) {
      const dashboardIndex = tabs.value.findIndex((tab) => tab.path === DASHBOARD_PATH)
      if (dashboardIndex === -1) {
        tabs.value = tabs.value.slice(index)
      } else if (dashboardIndex < index) {
        tabs.value = [tabs.value[dashboardIndex], ...tabs.value.slice(index)]
      } else {
        tabs.value = tabs.value.slice(index)
      }
    }
    activeTab.value = path
  }

  const closeRightTabs = (path: string): void => {
    const index = tabs.value.findIndex((tab) => tab.path === path)
    if (index > -1 && index < tabs.value.length - 1) {
      tabs.value = tabs.value.slice(0, index + 1)
    }
    activeTab.value = path
  }

  return {
    tabs,
    activeTab,
    addTab,
    removeTab,
    closeOtherTabs,
    closeAllTabs,
    closeLeftTabs,
    closeRightTabs
  }
})
