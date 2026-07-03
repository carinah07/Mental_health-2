import api from '@/services/api'

export async function downloadAssessmentReport(reportType, assessmentId) {
  const response = await api.get(
    `/api/assessment/reports/${reportType}/${assessmentId}/download/`,
    { responseType: 'blob' }
  )

  const url = window.URL.createObjectURL(new Blob([response.data]))
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', `mindcare-report-${assessmentId}.docx`)
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.URL.revokeObjectURL(url)
}

export async function fetchMyReports() {
  const { data } = await api.get('/api/assessment/reports/')
  return data
}
