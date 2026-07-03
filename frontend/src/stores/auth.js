import { defineStore } from 'pinia'
import api from '@/services/api'

const TOKEN_KEY = 'mindcare_access_token'
const REFRESH_KEY = 'mindcare_refresh_token'
const USER_KEY = 'mindcare_user'

function parseApiError(err, fallback) {
  const data = err?.response?.data
  if (!data) {
    return err?.message?.includes('Network Error')
      ? 'Cannot reach the server. Make sure the backend is running on port 8000.'
      : fallback
  }
  if (typeof data === 'string') return data
  if (data.detail) return String(data.detail)

  const messages = []
  for (const value of Object.values(data)) {
    if (Array.isArray(value)) messages.push(String(value[0]))
    else if (typeof value === 'string') messages.push(value)
  }
  return messages[0] || fallback
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: localStorage.getItem(TOKEN_KEY) || '',
    refreshToken: localStorage.getItem(REFRESH_KEY) || '',
    user: JSON.parse(localStorage.getItem(USER_KEY) || 'null'),
    loading: false,
    error: '',
  }),

  getters: {
    isAuthenticated: (state) => Boolean(state.accessToken),
    isAdmin: (state) => Boolean(state.user?.is_staff),
    displayName: (state) => state.user?.first_name || state.user?.username || 'User',
  },

  actions: {
    setSession(access, refresh, user = null) {
      this.accessToken = access
      this.refreshToken = refresh
      this.user = user
      localStorage.setItem(TOKEN_KEY, access)
      localStorage.setItem(REFRESH_KEY, refresh)
      if (user) {
        localStorage.setItem(USER_KEY, JSON.stringify(user))
      }
    },

    clearSession() {
      this.accessToken = ''
      this.refreshToken = ''
      this.user = null
      this.error = ''
      localStorage.removeItem(TOKEN_KEY)
      localStorage.removeItem(REFRESH_KEY)
      localStorage.removeItem(USER_KEY)
    },

    async register(payload) {
      this.loading = true
      this.error = ''
      try {
        await api.post('/api/auth/register/', payload)
        return await this.login({ username: payload.username, password: payload.password })
      } catch (err) {
        this.error = parseApiError(err, 'Registration failed. Please check your details and try again.')
        throw err
      } finally {
        this.loading = false
      }
    },

    async login(credentials) {
      this.loading = true
      this.error = ''
      try {
        const { data } = await api.post('/api/auth/login/', credentials)
        this.setSession(data.access, data.refresh)
        await this.fetchMe()
        return data
      } catch (err) {
        this.error = parseApiError(err, 'Invalid username or password.')
        throw err
      } finally {
        this.loading = false
      }
    },

    async fetchMe() {
      const { data } = await api.get('/api/auth/me/')
      this.user = data
      localStorage.setItem(USER_KEY, JSON.stringify(data))
      return data
    },

    logout() {
      this.clearSession()
    },
  },
})
