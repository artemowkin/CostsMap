<script setup>
import CostsList from '../components/CostsList.vue'
import Navigation from '../components/Navigation.vue'
import CostsIncomesNav from '../components/CostsIncomesNav.vue'
import ActionsMenu from '../components/ActionsMenu.vue'
import { useRouter } from 'vue-router';
import { checkAuthentication } from '../utils/authentication'
import { ref, Transition } from 'vue'
import { useCategoriesStore } from '../stores/categories'
import { useCostsStore } from '../stores/costs'
import { useCardsStore } from '../stores/cards'
import axios from '../axiosInstance'

const router = useRouter()

if ( !checkAuthentication() ) router.replace('/login')

const categoriesStore = useCategoriesStore()
const costsStore = useCostsStore()
const cardsStore = useCardsStore()

const selectedCostId = ref(null)
const showActionsMenu = ref(false)

const selectCost = (costId) => {
    selectedCostId.value = costId
}

const setShowActionsMenu = (value, costId) => {
    selectCost(costId)
    showActionsMenu.value = value
}

const deleteCostAction = async () => {
    const response = confirm('Are you sure?')

    if (!response) return

    const token = JSON.parse( localStorage.getItem('tokenData') ).token

    await axios.delete(`/costs/${selectedCostId.value}`, {
        headers: { Authorization: `Bearer ${token}` }
    })

    cardsStore.loadCards(true)
    categoriesStore.loadCategories(true)
    costsStore.loadCosts(true)

    setShowActionsMenu(false)
}
</script>

<template>
    <main class="costs_list_page">
        <CostsList :showForm="setShowActionsMenu" />
    </main>
    <CostsIncomesNav now="costs" />
    <Transition name="popup_form">
        <ActionsMenu v-if="showActionsMenu" :showForm="setShowActionsMenu" :deleteAction="deleteCostAction" />
    </Transition>
    <Navigation />
</template>

<style>
.costs_list_page {
    padding-bottom: 200px;
}
</style>
