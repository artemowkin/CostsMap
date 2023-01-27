import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import LoginView from '@/views/LoginView.vue'
import CategoriesView from '@/views/CategoriesView.vue'
import RegistrationView from '@/views/RegistrationView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/registration',
      name: 'registration',
      component: RegistrationView
    },
    {
      path: '/',
      name: 'categories',
      component: CategoriesView,
    },
  ]
})

const _loadUserData = async (userStore: any): Promise<{ name: string } | void> => {
  try {
    await userStore.refresh()
    await userStore.load()
  } catch (err: any) {
    switch (err?.response?.status) {
      case 401:
      case 403:
        return { name: 'login' }
      default:
        throw err
    }
  }
}

router.beforeEach(async (to) => {
  if (to.name === 'login' || to.name === 'registration') return

  const userStore = useUserStore()

  if (!userStore.accessToken || !userStore.refreshToken)
    return { name: 'login' }

  const redirect = await _loadUserData(userStore)

  if (redirect) return redirect

  if (!userStore.currentUser) return { name: 'login' }
})

export default router
