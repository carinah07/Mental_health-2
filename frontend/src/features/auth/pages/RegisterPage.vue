<template>
  <div class="auth-page">
    <div ref="vantaRef" class="vanta-background"></div>
    <div class="background-glow"></div>

    <div class="auth-card">
      <h1>{{ $t('register_title') }}</h1>
      <p class="subtitle">{{ $t('register_subtitle') }}</p>

      <form @submit.prevent="handleRegister">
        <label>{{ $t('full_name') }}</label>
        <input v-model="form.first_name" type="text" required />

        <label>{{ $t('username') }}</label>
        <input v-model="form.username" type="text" required autocomplete="username" />

        <label>{{ $t('email') }}</label>
        <input v-model="form.email" type="email" required autocomplete="email" />

        <label>{{ $t('password') }}</label>
        <PasswordInput v-model="form.password" autocomplete="new-password" :minlength="8" required />
        <p class="hint">{{ $t('password_hint') }}</p>

        <label>{{ $t('confirm_password') }}</label>
        <PasswordInput v-model="form.password_confirm" autocomplete="new-password" :minlength="8" required />

        <p v-if="auth.error" class="error">{{ auth.error }}</p>

        <button type="submit" :disabled="auth.loading">
          {{ auth.loading ? $t('please_wait') : $t('create_account') }}
        </button>
      </form>

      <p class="switch">
        {{ $t('have_account') }}
        <router-link to="/login">{{ $t('login') }}</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useVantaBackground } from '@/composables/useVantaBackground'
import PasswordInput from '@/shared/components/PasswordInput.vue'

const auth = useAuthStore()
const router = useRouter()
const { vantaRef } = useVantaBackground()

const form = reactive({
  first_name: '',
  username: '',
  email: '',
  password: '',
  password_confirm: '',
})

async function handleRegister() {
  if (form.password !== form.password_confirm) {
    auth.error = 'Passwords do not match.'
    return
  }
  try {
    await auth.register(form)
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
  margin-bottom: 0.25rem;
  background: var(--bg-card);
  color: var(--text-dark);
}

.hint {
  margin: 0 0 0.5rem;
  font-size: 0.82rem;
  color: var(--text-secondary);
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

.error {
  color: var(--danger);
  font-size: 0.9rem;
}

.switch {
  text-align: center;
  margin-top: 1.25rem;
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
