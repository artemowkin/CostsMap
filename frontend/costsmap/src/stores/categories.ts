import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useUserStore } from '@/stores/user'
import { apiFetch } from '@/globals'

export interface Category {
  uuid: string
  title: string
  limit: number
  color: string
}

const loadCategories = async (token: string): Promise<Category[]> => {
  const response = await apiFetch('/api/categories', {
    headers: { Authorization: `Bearer ${token}` }
  })
  return response as Category[]
}

export const useCategoriesStore = defineStore('categories', () => {
  const userStore = useUserStore()

  const categories = ref<Category[]>([])

  const load = async () => {
    const loadedCategories = await loadCategories(userStore.accessToken!)
    categories.value = loadedCategories
  }

  return { categories, load }
})