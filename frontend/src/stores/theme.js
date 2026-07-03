import { defineStore } from 'pinia'

const THEME_KEY = 'mindcare_theme'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    isDark: localStorage.getItem(THEME_KEY) === 'dark',
  }),

  actions: {
    toggle() {
      this.isDark = !this.isDark
      this.apply()
    },
    setDark(val) {
      this.isDark = val
      this.apply()
    },
    apply() {
      localStorage.setItem(THEME_KEY, this.isDark ? 'dark' : 'light')
      document.documentElement.setAttribute('data-theme', this.isDark ? 'dark' : 'light')
    },
  },
})
