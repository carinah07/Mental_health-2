<template>
  <div class="admin-page">
    <header class="navbar">
      <div class="nav-left">
        <h2 class="brand-name">MindCare Admin</h2>
      </div>
      <nav class="nav-links">
        <a @click="$router.push('/mental-health')" class="nav-link">{{ $t('user_dashboard') }}</a>
        <span class="user-greeting">{{ $t('welcome_user') }}, {{ auth.displayName }}</span>
        <a @click="handleLogout" class="nav-link">{{ $t('logout') }}</a>
        <ThemeToggle />
      </nav>
    </header>

    <h1>{{ $t('admin_panel') }}</h1>
    <p class="sub">{{ $t('admin_panel_desc') }}</p>

    <div class="panels">
      <section class="card">
        <h2>{{ $t('add_user') }}</h2>
        <form @submit.prevent="handleCreate">
          <label>{{ $t('full_name') }}</label>
          <input v-model="form.first_name" type="text" required />

          <label>{{ $t('username') }}</label>
          <input v-model="form.username" type="text" required />

          <label>{{ $t('email') }}</label>
          <input v-model="form.email" type="email" required />

          <label>{{ $t('password') }}</label>
          <PasswordInput v-model="form.password" autocomplete="new-password" :minlength="8" required />

          <label>{{ $t('confirm_password') }}</label>
          <PasswordInput v-model="form.password_confirm" autocomplete="new-password" :minlength="8" required />

          <label class="checkbox-row">
            <input v-model="form.is_staff" type="checkbox" />
            {{ $t('admin_user') }}
          </label>

          <p v-if="error" class="error">{{ error }}</p>
          <p v-if="success" class="success">{{ success }}</p>

          <button type="submit" :disabled="saving">
            {{ saving ? $t('please_wait') : $t('add_user') }}
          </button>
        </form>
      </section>

      <section class="card users-card">
        <h2>{{ $t('manage_users') }}</h2>
        <div v-if="loading" class="muted">{{ $t('please_wait') }}</div>
        <div v-else-if="users.length === 0" class="muted">{{ $t('no_users') }}</div>
        <div v-else class="user-list">
          <div v-for="user in users" :key="user.id" class="user-row">
            <div>
              <strong>{{ user.first_name || user.username }}</strong>
              <p>@{{ user.username }} · {{ user.email }}</p>
              <span class="badge" :class="{ admin: user.is_staff }">
                {{ user.is_staff ? $t('admin_user') : $t('regular_user') }}
              </span>
            </div>
            <div class="user-actions">
              <button class="secondary" @click="selectUserForReports(user)">
                {{ $t('view_reports') }}
              </button>
              <button
                v-if="user.id !== auth.user?.id"
                class="danger"
                :disabled="deletingId === user.id"
                @click="handleDelete(user)"
              >
                {{ $t('remove_user') }}
              </button>
              <span v-else class="muted small">{{ $t('current_account') }}</span>
            </div>
          </div>
        </div>
      </section>
    </div>

    <section class="card reports-card">
      <h2>{{ $t('user_reports') }}</h2>
      <p class="muted">{{ $t('user_reports_desc') }}</p>

      <label>{{ $t('select_user') }}</label>
      <select v-model="selectedUserId" @change="loadUserReports">
        <option value="">{{ $t('choose_user') }}</option>
        <option v-for="user in users" :key="user.id" :value="user.id">
          {{ user.first_name || user.username }} (@{{ user.username }})
        </option>
      </select>

      <div v-if="reportsLoading" class="muted">{{ $t('please_wait') }}</div>
      <div v-else-if="selectedUserId && userReports.length === 0" class="muted">
        {{ $t('no_user_reports') }}
      </div>
      <div v-else-if="userReports.length" class="report-list">
        <div v-for="report in userReports" :key="`${report.type}-${report.id}`" class="report-row">
          <div>
            <strong>{{ report.title }}</strong>
            <p>{{ $t('your_score') }}: {{ report.score }} / {{ report.max_score }}</p>
            <p>{{ $t('severity') }}: {{ report.severity }}</p>
            <p class="date">{{ formatDate(report.created_at) }}</p>
          </div>
          <button
            :disabled="downloadingKey === `${report.type}-${report.id}`"
            @click="handleDownloadReport(report)"
          >
            {{ $t('download_report') }}
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import ThemeToggle from '@/shared/components/ThemeToggle.vue'
import PasswordInput from '@/shared/components/PasswordInput.vue'
import { fetchUsers, createUser, deleteUser, fetchUserReports, downloadUserReport } from '@/services/admin'

const auth = useAuthStore()
const router = useRouter()

const users = ref([])
const loading = ref(true)
const saving = ref(false)
const deletingId = ref(null)
const error = ref('')
const success = ref('')
const selectedUserId = ref('')
const userReports = ref([])
const reportsLoading = ref(false)
const downloadingKey = ref('')

const form = reactive({
  first_name: '',
  username: '',
  email: '',
  password: '',
  password_confirm: '',
  is_staff: false,
})

async function loadUsers() {
  loading.value = true
  try {
    users.value = await fetchUsers()
  } finally {
    loading.value = false
  }
}

async function handleCreate() {
  error.value = ''
  success.value = ''
  if (form.password !== form.password_confirm) {
    error.value = 'Passwords do not match.'
    return
  }
  saving.value = true
  try {
    await createUser({ ...form })
    success.value = 'User added successfully.'
    form.first_name = ''
    form.username = ''
    form.email = ''
    form.password = ''
    form.password_confirm = ''
    form.is_staff = false
    await loadUsers()
  } catch (err) {
    const data = err?.response?.data
    error.value = data?.username?.[0] || data?.email?.[0] || data?.detail || 'Could not add user.'
  } finally {
    saving.value = false
  }
}

async function handleDelete(user) {
  if (!window.confirm(`Remove user "${user.username}"?`)) return
  deletingId.value = user.id
  error.value = ''
  try {
    await deleteUser(user.id)
    success.value = `Removed ${user.username}.`
    if (String(selectedUserId.value) === String(user.id)) {
      selectedUserId.value = ''
      userReports.value = []
    }
    await loadUsers()
  } catch (err) {
    error.value = err?.response?.data?.detail || 'Could not remove user.'
  } finally {
    deletingId.value = null
  }
}

function formatDate(iso) {
  return new Date(iso).toLocaleString()
}

function selectUserForReports(user) {
  selectedUserId.value = String(user.id)
  loadUserReports()
}

async function loadUserReports() {
  userReports.value = []
  if (!selectedUserId.value) return

  reportsLoading.value = true
  error.value = ''
  try {
    const data = await fetchUserReports(selectedUserId.value)
    userReports.value = data.reports || []
  } catch (err) {
    error.value = err?.response?.data?.error || err?.response?.data?.detail || 'Could not load user reports.'
  } finally {
    reportsLoading.value = false
  }
}

async function handleDownloadReport(report) {
  const key = `${report.type}-${report.id}`
  downloadingKey.value = key
  error.value = ''
  try {
    await downloadUserReport(selectedUserId.value, report.type, report.id)
    success.value = 'Report downloaded successfully.'
  } catch (err) {
    error.value = err?.response?.data?.error || 'Could not download report.'
  } finally {
    downloadingKey.value = ''
  }
}

function handleLogout() {
  auth.logout()
  router.push('/login')
}

onMounted(loadUsers)
</script>

<style scoped>
.admin-page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 1rem 2rem 3rem;
}

.navbar {
  background: var(--bg-navbar);
  padding: 1rem 1.5rem;
  border-radius: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.brand-name {
  color: var(--primary-teal);
  margin: 0;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.nav-link {
  color: var(--primary-teal);
  font-weight: 600;
  cursor: pointer;
}

.user-greeting {
  color: var(--primary-teal-dark);
  font-weight: 600;
}

h1 {
  color: var(--primary-teal-dark);
  margin-bottom: 0.25rem;
}

.sub {
  color: var(--text-muted);
  margin-bottom: 1.5rem;
}

.panels {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 1.5rem;
}

.card {
  background: var(--bg-card);
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 18px var(--shadow-card);
  border-left: 5px solid var(--primary-teal);
}

form {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

label {
  font-weight: 600;
  color: var(--primary-teal);
  font-size: 0.9rem;
}

input[type='text'],
input[type='email'] {
  padding: 0.7rem 1rem;
  border: 1px solid var(--border-input);
  border-radius: 10px;
  margin-bottom: 0.35rem;
  background: var(--bg-card);
  color: var(--text-dark);
}

.checkbox-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0.5rem 0;
}

button {
  margin-top: 0.5rem;
  padding: 0.8rem;
  background: var(--primary-teal);
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
}

button.danger {
  background: var(--danger);
  margin-top: 0;
  padding: 0.55rem 0.9rem;
}

button.secondary {
  background: var(--primary-teal-dark);
  margin-top: 0;
  padding: 0.55rem 0.9rem;
}

.user-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  align-items: flex-end;
}

.reports-card {
  margin-top: 1.5rem;
}

select {
  width: 100%;
  max-width: 420px;
  padding: 0.7rem 1rem;
  border: 1px solid var(--border-input);
  border-radius: 10px;
  margin: 0.5rem 0 1rem;
  background: var(--bg-card);
  color: var(--text-dark);
}

.report-list {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.report-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding: 0.9rem 1rem;
  border: 1px solid var(--border-card);
  border-radius: 12px;
}

.report-row p {
  margin: 0.15rem 0;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.date {
  font-size: 0.82rem;
  color: var(--text-footer);
}

.user-list {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.user-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding: 0.9rem 1rem;
  border: 1px solid var(--border-card);
  border-radius: 12px;
}

.user-row p {
  margin: 0.2rem 0;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.badge {
  display: inline-block;
  margin-top: 0.35rem;
  padding: 0.15rem 0.55rem;
  border-radius: 999px;
  background: var(--badge-bg);
  color: var(--badge-text);
  font-size: 0.78rem;
  font-weight: 700;
}

.badge.admin {
  background: var(--bg-hover-teal);
  color: var(--primary-teal-dark);
}

.error {
  color: var(--danger);
}

.success {
  color: var(--primary-teal-dark);
}

.muted {
  color: var(--text-secondary);
}

.small {
  font-size: 0.85rem;
}

@media (max-width: 900px) {
  .panels {
    grid-template-columns: 1fr;
  }
}
</style>
