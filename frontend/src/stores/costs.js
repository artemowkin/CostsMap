import { defineStore } from 'pinia'
import axios from '../axiosInstance'

export const useCostsStore = defineStore({
  id: 'costs',

  state: () => ({
    monthCosts: 0,
  }),

  actions: {
    async loadMonthCosts() {
      const token = JSON.parse( localStorage.getItem('tokenData') ).token

      const response = await axios.get('/costs/total/', {
        headers: { Authorization: `Bearer ${token}` }
      })

      this.monthCosts = response.data.totalCosts
    }
  },
})
