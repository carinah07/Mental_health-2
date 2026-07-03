import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import MentalHealthHome from '@/features/home/pages/MentalHealthHome.vue'
import LandingPage from '@/features/home/pages/LandingPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: LandingPage,
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/features/auth/pages/LoginPage.vue'),
      meta: { guestOnly: true },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/features/auth/pages/RegisterPage.vue'),
      meta: { guestOnly: true },
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('@/features/admin/pages/AdminDashboard.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
      path: '/mental-health',
      name: 'mental-health',
      component: MentalHealthHome,
      meta: { requiresAuth: true },
    },
    {
      path: '/my-reports',
      name: 'my-reports',
      component: () => import('@/features/reports/pages/MyReportsPage.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/followup/:id',
      name: 'FollowupForm',
      component: () => import('@/features/followup/pages/FollowupForm.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/followup/child/:id',
      name: 'ChildFollowupForm',
      component: () => import('@/features/followup/pages/ChildFollowUp.vue'),
      meta: { requiresAuth: true },
    },
  ],
})

function defaultAuthedRoute(auth) {
  return auth.isAdmin ? { name: 'admin' } : { name: 'mental-health' }
}

router.beforeEach((to) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (to.meta.requiresAdmin && !auth.isAdmin) {
    return { name: 'mental-health' }
  }

  if (to.meta.guestOnly && auth.isAuthenticated) {
    return defaultAuthedRoute(auth)
  }

  return true
})

export default router
