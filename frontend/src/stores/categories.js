import { defineStore } from 'pinia'
import axios from '../axiosInstance'

export const useCategoriesStore = defineStore({
  id: 'categories',

  state: () => ({
    categories: [],
  }),

  actions: {
    async loadCategories(reload=false) {
      if (this.categories.length === 0 || reload) {
        const token = JSON.parse( localStorage.getItem('tokenData') ).token

        const response = await axios.get('/categories/', {
          headers: { Authorization: `Bearer ${token}` }
        })

        this.categories = response.data
      }
    }
  },
})
