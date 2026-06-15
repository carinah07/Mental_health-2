import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { createI18n } from 'vue-i18n'
import en from './i18n/en.json'
import sw from './i18n/sw.json'

const i18n = createI18n({
  locale: 'en',
  fallbackLocale: 'en',
  messages: { en, sw }
})

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(i18n)
app.mount('#app')
