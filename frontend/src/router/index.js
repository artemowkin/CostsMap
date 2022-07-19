import { createRouter, createWebHistory } from 'vue-router'
import { checkAuthentication } from '../utils/authentication'
import LoginView from '../views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: () => ({ path: '/categories' })
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginView
    },
  ]
})

router.beforeEach((to, from) => {
  const isAuthenticated = checkAuthentication() 

  if (to.name !== 'Login' && !isAuthenticated)
    return { name: 'Login' }
})

export default router
