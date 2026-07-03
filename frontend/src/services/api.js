import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const instance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
  headers: {
    'X-Requested-With': 'XMLHttpRequest',
  },
})

instance.interceptors.request.use((config) => {
  const auth = useAuthStore()
  if (auth.accessToken) {
    config.headers.Authorization = `Bearer ${auth.accessToken}`
  }
  return config
})

instance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const auth = useAuthStore()
    const original = error.config

    if (error.response?.status === 401 && !original._retry && auth.refreshToken) {
      original._retry = true
      try {
        const { data } = await axios.post(
          `${instance.defaults.baseURL}/api/auth/refresh/`,
          { refresh: auth.refreshToken }
        )
        auth.setSession(data.access, auth.refreshToken, auth.user)
        original.headers.Authorization = `Bearer ${data.access}`
        return instance(original)
      } catch {
        auth.logout()
      }
    }

    return Promise.reject(error)
  }
)

export default instance
