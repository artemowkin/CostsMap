import { createRouter, createWebHistory } from 'vue-router'
import { checkAuthentication } from '@/utils/authentication'
import LoginView from '@/views/LoginView.vue'
import RegistrationView from '@/views/RegistrationView.vue'
import CategoriesView from '@/views/CategoriesView.vue'
import EditCategoriesView from '@/views/EditCategoriesView.vue'
import CardsView from '@/views/CardsView.vue'
import CostsView from '@/views/CostsView.vue'
import IncomesView from '@/views/IncomesView.vue'

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
    {
      path: '/registration',
      name: 'Registration',
      component: RegistrationView
    },
    {
      path: '/categories',
      name: 'Categories',
      component: CategoriesView
    },
    {
      path: '/edit_categories',
      name: 'EditCategories',
      component: EditCategoriesView
    },
    {
      path: '/cards',
      name: 'Cards',
      component: CardsView
    },
    {
      path: '/costs',
      name: 'Costs',
      component: CostsView
    },
    {
      path: '/incomes',
      name: 'Incomes',
      component: IncomesView
    }
  ]
})

router.beforeEach((to, from) => {
  const isAuthenticated = checkAuthentication() 

  if (to.name !== 'Login' && to.name !== 'Registration' && !isAuthenticated)
    return { name: 'Login' }
})

export default router
