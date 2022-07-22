import { defineStore } from 'pinia'
import axios from '../axiosInstance'

export const useIncomesStore = defineStore({
  id: 'incomes',

  state: () => ({
    monthIncomes: 0,
    incomes: []
  }),

  getters: {
    datedIncomes() {
      const datedIncomesObj = {}

      const incomesDates = this.incomes.map(income => income.date)

      incomesDates.forEach((incomeDate) => {
        const dateIncomes = this.incomes.filter((income) => income.date === incomeDate)
        const totalDateIncomes = dateIncomes.reduce((total, income) => total + income.userCurrencyAmount, 0)
        datedIncomesObj[incomeDate] = { incomes: dateIncomes, total: totalDateIncomes }
      })

      return datedIncomesObj
    }
  },

  actions: {
    async loadMonthIncomes() {
      const token = JSON.parse( localStorage.getItem('tokenData') ).token

      const response = await axios.get('/incomes/total/', {
        headers: { Authorization: `Bearer ${token}` }
      })

      this.monthIncomes = response.data.totalIncomes
    },

    async loadIncomes(reload=false) {
      if (this.incomes.length === 0 || reload) {
        const token = JSON.parse( localStorage.getItem('tokenData') ).token

        const response = await axios.get('/incomes/', {
          headers: { Authorization: `Bearer ${token}` }
        })

        this.incomes = response.data
      }
    }
  },
})
