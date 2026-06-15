import { createRouter, createWebHistory } from 'vue-router'
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
      path: '/mental-health',
      name: 'mental-health',
      component: MentalHealthHome,
    },
    {
      path: '/followup/:id',
      name: 'FollowupForm',
      component: () => import('@/features/followup/pages/FollowupForm.vue')
    },
    {
      path: '/followup/child/:id',
      name: 'ChildFollowupForm',
      component: () => import('@/features/followup/pages/ChildFollowUp.vue')
    },
  ],
})

export default router
