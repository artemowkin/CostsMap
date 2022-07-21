import { defineStore } from 'pinia'
import axios from '../axiosInstance'

export const useCostsStore = defineStore({
  id: 'costs',

  state: () => ({
    monthCosts: 0,
    costs: []
  }),

  getters: {
    datedCosts() {
      const datedCostsObj = {}

      const costsDates = this.costs.map(cost => cost.date)

      costsDates.forEach((costDate) => {
        const dateCosts = this.costs.filter((cost) => cost.date === costDate)
        const totalDateCosts = dateCosts.reduce((total, cost) => total + cost.userCurrencyAmount, 0)
        datedCostsObj[costDate] = { costs: dateCosts, total: totalDateCosts }
      })

      return datedCostsObj
    }
  },

  actions: {
    async loadMonthCosts() {
      const token = JSON.parse( localStorage.getItem('tokenData') ).token

      const response = await axios.get('/costs/total/', {
        headers: { Authorization: `Bearer ${token}` }
      })

      this.monthCosts = response.data.totalCosts
    },

    async loadCosts() {
      const token = JSON.parse( localStorage.getItem('tokenData') ).token

      const response = await axios.get('/costs/', {
        headers: { Authorization: `Bearer ${token}` }
      })

      this.costs = response.data
    }
  },
})
