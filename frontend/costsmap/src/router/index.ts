import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import LoginView from '@/views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
  ]
})

router.beforeEach(async (to) => {
  if (to.name === 'login') return

  const userStore = useUserStore()

  await userStore.load()

  if (!userStore.currentUser) return { name: 'login' }
})

export default router
