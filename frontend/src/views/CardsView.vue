<script setup>
import CardsList from '../components/CardsList.vue'
import Navigation from '../components/Navigation.vue'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { checkAuthentication } from '../utils/authentication'
import AddButton from '../components/AddButton.vue'
import AddCardForm from '../components/AddCardForm.vue'
import ActionsMenu from '../components/ActionsMenu.vue'
import axios from '../axiosInstance'
import { useCardsStore } from '../stores/cards'
import { useCategoriesStore } from '../stores/categories'
import { useCostsStore } from '../stores/costs'
import { useIncomesStore } from '../stores/incomes'

const router = useRouter()

if ( !checkAuthentication() ) router.replace('/login')

const cardsStore = useCardsStore()
const categoriesStore = useCategoriesStore()
const costsStore = useCostsStore()
const incomesStore = useIncomesStore()

const showAddCardForm = ref(false)
const showActionsMenu = ref(false)
const selectedCardId = ref(null)

const setShowAddCardForm = (value) => {
    showAddCardForm.value = value
}

const selectCard = (cardId) => {
    selectedCardId.value = cardId
}

const setShowActionsMenu = (value, cardId) => {
    selectCard(cardId)
    showActionsMenu.value = value
}

const deleteCardAction = async () => {
    const response = confirm('Are you sure?')

    if (!response) return

    const token = JSON.parse( localStorage.getItem('tokenData') ).token

    await axios.delete(`/cards/${selectedCardId.value}`, {
        headers: { Authorization: `Bearer ${token}` }
    })

    cardsStore.loadCards(true)
    categoriesStore.loadCategories(true)
    costsStore.loadMonthCosts()
    costsStore.loadCosts(true)
    incomesStore.loadIncomes(true)

    setShowActionsMenu(false)
}
</script>

<template>
    <main>
        <CardsList :showForm="setShowActionsMenu" />
    </main>
    <AddButton :showForm="setShowAddCardForm" />
    <Transition name="popup_form">
        <AddCardForm v-if="showAddCardForm" :setShowAddCard="setShowAddCardForm" />
    </Transition>
    <Transition name="popup_form">
        <ActionsMenu v-if="showActionsMenu" :showForm="setShowActionsMenu" :deleteAction="deleteCardAction" />
    </Transition>
    <Navigation />
</template>