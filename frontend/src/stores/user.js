import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login as loginApi } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('admin_token') || '')
  const isAdmin = ref(!!token.value)

  const login = async (username, password) => {
    const res = await loginApi({ username, password })
    token.value = res.access_token
    isAdmin.value = true
    localStorage.setItem('admin_token', res.access_token)
  }

  const logout = () => {
    token.value = ''
    isAdmin.value = false
    localStorage.removeItem('admin_token')
  }

  return {
    token,
    isAdmin,
    login,
    logout
  }
})
