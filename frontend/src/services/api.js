import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

// Fall back to localhost for local development, or the Railway-hosted
// backend when no explicit VITE_API_BASE_URL is provided (e.g. production
// builds that were not configured with the env var).
const defaultBaseURL = import.meta.env.DEV
  ? 'http://127.0.0.1:8000'
  : 'https://mentalpals.up.railway.app'

const instance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || defaultBaseURL,
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
