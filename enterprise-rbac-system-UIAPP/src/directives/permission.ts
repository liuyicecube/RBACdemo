import type { Directive, DirectiveBinding } from 'vue'
import { useUserStore } from '@/store'

export const permission: Directive = {
  mounted(el: HTMLElement, binding: DirectiveBinding) {
    const userStore = useUserStore()
    const permission = binding.value
    
    if (permission && !userStore.hasPermission(permission)) {
      el.parentNode?.removeChild(el)
    }
  }
}
