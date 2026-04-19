import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useTabsStore } from '../modules/tabs'

describe('Tabs Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should initialize with empty tabs', () => {
    const store = useTabsStore()
    expect(store.tabs).toEqual([])
    expect(store.activeTab).toBe('')
  })

  it('should add a tab', () => {
    const store = useTabsStore()
    const tab = { name: 'dashboard', title: 'Dashboard', path: '/dashboard' }
    store.addTab(tab)
    expect(store.tabs).toHaveLength(1)
    expect(store.tabs[0]).toEqual(tab)
    expect(store.activeTab).toBe(tab.name)
  })

  it('should not add duplicate tabs', () => {
    const store = useTabsStore()
    const tab = { name: 'dashboard', title: 'Dashboard', path: '/dashboard' }
    store.addTab(tab)
    store.addTab(tab)
    expect(store.tabs).toHaveLength(1)
  })

  it('should remove a tab', () => {
    const store = useTabsStore()
    const tab1 = { name: 'dashboard', title: 'Dashboard', path: '/dashboard' }
    const tab2 = { name: 'users', title: 'Users', path: '/users' }
    store.addTab(tab1)
    store.addTab(tab2)
    store.removeTab('dashboard')
    expect(store.tabs).toHaveLength(1)
    expect(store.tabs[0].name).toBe('users')
  })

  it('should set active tab', () => {
    const store = useTabsStore()
    const tab = { name: 'dashboard', title: 'Dashboard', path: '/dashboard' }
    store.addTab(tab)
    store.setActiveTab('dashboard')
    expect(store.activeTab).toBe('dashboard')
  })
})
