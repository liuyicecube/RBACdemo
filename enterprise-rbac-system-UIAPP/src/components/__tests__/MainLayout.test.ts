import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../layout/MainLayout.vue'

describe('MainLayout Component', () => {
  const pinia = createPinia()
  const router = createRouter({
    history: createWebHistory(),
    routes: [{ path: '/', component: { template: '<div />' } }]
  })

  it('should render without crashing', () => {
    const wrapper = mount(MainLayout, {
      global: {
        plugins: [pinia, router],
        stubs: ['router-view', 'router-link']
      }
    })
    expect(wrapper.exists()).toBe(true)
  })

  it('should have a sidebar', () => {
    const wrapper = mount(MainLayout, {
      global: {
        plugins: [pinia, router],
        stubs: ['router-view', 'router-link']
      }
    })
    expect(wrapper.find('.sidebar').exists()).toBe(true)
  })
})
