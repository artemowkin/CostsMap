import { defineStore } from 'pinia'
import axios from '../axiosInstance'

export const useUserStore = defineStore({
  id: 'user',

  state: () => ({
    user: {}
  }),

  actions: {
    async loadUser(reload=false) {
      if (!this.user.email || reload) {
        const token = JSON.parse( localStorage.getItem('tokenData') ).token

        const response = await axios.get('/auth/me/', {
          headers: { Authorization: `Bearer ${token}` }
        })

        this.user = response.data
      }
    }
  },
})
