import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const isLogin = ref(false)
  const username = ref('')
  const email = ref('')

  const setLogin = ({ username: name, email: addr }) => {
    isLogin.value = true
    username.value = name
    email.value = addr
    console.log("✅ 로그인 상태 설정됨:", name)
  }

  const logout = () => {
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refresh')
    isLogin.value = false
    username.value = ''
    email.value = ''
    console.warn("🚪 로그아웃 처리됨")
  }

  const refreshAccessToken = async () => {
    const refresh = localStorage.getItem('refresh')
    if (!refresh) return false

    try {
      const res = await axios.post('http://localhost:8000/api/v1/accounts/token/refresh/', {
        refresh
      })

      localStorage.setItem('accessToken', res.data.access)

      setLogin({
        username: res.data.username ?? '닉네임없음',
        email: res.data.email ?? ''
      })

      return true
    } catch (err) {
      logout()
      return false
    }
  }

  const initializeAuth = async () => {
    console.log("🔐 initializeAuth 시작")
    const token = localStorage.getItem('accessToken')
    if (!token) {
      console.warn("❌ accessToken 없음")
      return
    }

    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      const exp = payload.exp * 1000
      const now = Date.now()

      if (now > exp) {
        console.log("⏰ accessToken 만료됨 → refresh 시도")
        const refreshed = await refreshAccessToken()
        if (!refreshed) logout()
      } else {
        console.log("✅ accessToken 유효 → 로그인 상태 복원")
        setLogin({
          username: payload.username ?? '닉네임없음',
          email: payload.email ?? ''
        })
      }
    } catch (err) {
      console.error("💥 JWT 디코딩 실패:", err.message)
      logout()
    }
  }

  return {
    isLogin,
    username,
    email,
    setLogin,
    logout,
    initializeAuth,
    refreshAccessToken,
  }
})
