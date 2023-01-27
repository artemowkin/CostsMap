import type { Category } from '@/interfaces/categories'
import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useUserStore } from '@/stores/user'
import { loadCategories } from '@/api/categories'

export const useCategoriesStore = defineStore('categories', () => {
  const userStore = useUserStore()

  const categories = ref<Category[]>([])

  const load = async () => {
    const loadedCategories = await loadCategories(userStore.accessToken!)
    categories.value = loadedCategories
  }

  return { categories, load }
})