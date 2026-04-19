import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import App from './App.vue'
import router from './router'
import pinia from './store'
import { permission } from './directives/permission'
import '@/styles/global.scss'

const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(ElementPlus)
app.use(router)
app.use(pinia)
app.directive('permission', permission)

// Set ElMessage._context to app's context
ElMessage._context = app._context

app.mount('#app')
