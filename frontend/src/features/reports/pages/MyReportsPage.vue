<template>
  <div class="reports-page">
    <header class="navbar">
      <div class="nav-left">
        <h2 class="brand-name">MindCare</h2>
      </div>
      <nav class="nav-links">
        <a @click="$router.push('/mental-health')" class="nav-link">{{ $t('dashboard') }}</a>
        <a @click="handleLogout" class="nav-link">{{ $t('logout') }}</a>
        <ThemeToggle />
      </nav>
    </header>

    <h1>{{ $t('my_reports') }}</h1>
    <p class="sub">{{ $t('my_reports_desc') }}</p>

    <div v-if="loading" class="loading">{{ $t('please_wait') }}</div>

    <div v-else-if="reports.length === 0" class="empty">
      {{ $t('no_reports') }}
    </div>

    <div v-else class="report-list">
      <div v-for="report in reports" :key="`${report.type}-${report.id}`" class="report-card">
        <div>
          <h3>{{ report.title }}</h3>
          <p>{{ $t('your_score') }}: {{ report.score }} / {{ report.max_score }}</p>
          <p>{{ $t('severity') }}: {{ report.severity }}</p>
          <p class="date">{{ formatDate(report.created_at) }}</p>
        </div>
        <button @click="download(report)" :disabled="downloadingId === `${report.type}-${report.id}`">
          {{ $t('download_report') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import ThemeToggle from '@/shared/components/ThemeToggle.vue'
import { fetchMyReports, downloadAssessmentReport } from '@/utils/reports'

const router = useRouter()
const auth = useAuthStore()
const reports = ref([])
const loading = ref(true)
const downloadingId = ref('')

onMounted(async () => {
  try {
    reports.value = await fetchMyReports()
  } finally {
    loading.value = false
  }
})

function formatDate(iso) {
  return new Date(iso).toLocaleString()
}

async function download(report) {
  const key = `${report.type}-${report.id}`
  downloadingId.value = key
  try {
    await downloadAssessmentReport(report.type, report.id)
  } finally {
    downloadingId.value = ''
  }
}

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.reports-page {
  max-width: 900px;
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
}

.brand-name {
  color: var(--primary-teal);
  margin: 0;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.nav-link {
  color: var(--primary-teal);
  font-weight: 600;
  cursor: pointer;
}

h1 {
  color: var(--primary-teal-dark);
}

.sub {
  color: var(--text-muted);
  margin-bottom: 1.5rem;
}

.report-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.report-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  background: var(--bg-card);
  border-left: 5px solid var(--primary-teal);
  border-radius: 12px;
  padding: 1.25rem;
  box-shadow: 0 4px 14px var(--shadow-card);
}

.report-card h3 {
  margin: 0 0 0.35rem;
  color: var(--primary-teal);
}

.report-card p {
  margin: 0.15rem 0;
  color: var(--text-subtle);
}

.date {
  font-size: 0.85rem;
  color: var(--text-footer);
}

button {
  background: var(--primary-teal);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 0.75rem 1rem;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
}

.empty, .loading {
  text-align: center;
  color: var(--text-secondary);
  padding: 2rem;
}
</style>
