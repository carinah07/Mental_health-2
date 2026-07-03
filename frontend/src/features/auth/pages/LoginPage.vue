<template>
  <div class="auth-page">
    <div ref="vantaRef" class="vanta-background"></div>
    <div class="background-glow"></div>

    <div class="auth-card">
      <div class="logo-wrap">
        <svg width="56" height="56" viewBox="0 0 72 72" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="36" cy="36" r="34" fill="#e6fff9" stroke="#0d9488" stroke-width="3"/>
          <path d="M22 30c0-7.7 6.3-14 14-14s14 6.3 14 14c0 5.2-2.8 9.7-7 12.2V52H29V42.2C24.8 39.7 22 35.2 22 30z" stroke="#0d9488" stroke-width="2.5" stroke-linejoin="round" fill="#f0fdfa"/>
        </svg>
      </div>
      <h1>{{ $t('login_title') }}</h1>
      <p class="subtitle">{{ $t('login_subtitle') }}</p>

      <form @submit.prevent="handleLogin">
        <label>{{ $t('username') }}</label>
        <input v-model="form.username" type="text" required autocomplete="username" />

        <label>{{ $t('password') }}</label>
        <PasswordInput v-model="form.password" autocomplete="current-password" required />

        <p v-if="auth.error" class="error">{{ auth.error }}</p>

        <button type="submit" :disabled="auth.loading">
          {{ auth.loading ? $t('please_wait') : $t('login') }}
        </button>
      </form>

      <p class="switch">
        {{ $t('no_account') }}
        <router-link to="/register">{{ $t('register') }}</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useVantaBackground } from '@/composables/useVantaBackground'
import PasswordInput from '@/shared/components/PasswordInput.vue'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()
const { vantaRef } = useVantaBackground()

const form = reactive({
  username: '',
  password: '',
})

async function handleLogin() {
  try {
    await auth.login(form)
    const redirect = route.query.redirect
    if (redirect) {
      router.push(redirect)
      return
    }
    router.push(auth.isAdmin ? '/admin' : '/mental-health')
  } catch {
    // error shown in template
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-page-gradient);
  padding: 1rem;
  position: relative;
  overflow: hidden;
}

.vanta-background {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.background-glow {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at center, #5eead444, transparent 60%);
  animation: pulse 8s infinite;
  z-index: 1;
  pointer-events: none;
}

.auth-card {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 420px;
  background: var(--bg-card-translucent);
  backdrop-filter: blur(8px);
  border-radius: 1.5rem;
  padding: 2rem;
  box-shadow: 0 12px 40px var(--shadow-card);
  border: 1px solid var(--border-card);
}

.logo-wrap {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
}

h1 {
  text-align: center;
  color: var(--primary-teal-dark);
  margin: 0 0 0.5rem;
}

.subtitle {
  text-align: center;
  color: var(--text-muted);
  margin-bottom: 1.5rem;
}

form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-weight: 600;
  color: var(--primary-teal);
  font-size: 0.9rem;
}

input {
  padding: 0.75rem 1rem;
  border: 1px solid var(--border-input);
  border-radius: 10px;
  margin-bottom: 0.5rem;
  font-size: 1rem;
  background: var(--bg-card);
  color: var(--text-dark);
}

button {
  margin-top: 0.5rem;
  padding: 0.85rem;
  background: var(--primary-teal);
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error {
  color: var(--danger);
  font-size: 0.9rem;
}

.switch {
  text-align: center;
  margin-top: 1.25rem;
  color: var(--text-muted);
}

.switch a {
  color: var(--primary-teal);
  font-weight: 700;
  text-decoration: none;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.7; }
  50% { transform: scale(1.1); opacity: 1; }
}
</style>
