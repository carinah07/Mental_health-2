import api from '@/services/api'

export async function fetchUsers() {
  const { data } = await api.get('/api/auth/admin/users/')
  return data
}

export async function createUser(payload) {
  const { data } = await api.post('/api/auth/admin/users/', payload)
  return data
}

export async function deleteUser(userId) {
  await api.delete(`/api/auth/admin/users/${userId}/`)
}

export async function fetchUserReports(userId) {
  const { data } = await api.get(`/api/assessment/admin/users/${userId}/reports/`)
  return data
}

export async function downloadUserReport(userId, reportType, assessmentId) {
  const response = await api.get(
    `/api/assessment/admin/users/${userId}/reports/${reportType}/${assessmentId}/download/`,
    { responseType: 'blob' }
  )

  const url = window.URL.createObjectURL(new Blob([response.data]))
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', `mindcare-report-user-${userId}-${assessmentId}.docx`)
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.URL.revokeObjectURL(url)
}
