import { defineStore } from 'pinia'
import axios from '../axiosInstance'

export const useCardsStore = defineStore({
  id: 'cards',

  state: () => ({
    cards: [],
  }),

  actions: {
    async loadCards(reload=false) {
      if (this.cards.length === 0 || reload) {
        const token = JSON.parse( localStorage.getItem('tokenData') ).token

        const response = await axios.get('/cards/', {
          headers: { Authorization: `Bearer ${token}` }
        })

        this.cards = response.data
      }
    }
  },
})
