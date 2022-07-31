<script setup>
import IncomesList from '../components/IncomesList.vue'
import Navigation from '../components/Navigation.vue'
import CostsIncomesNav from '../components/CostsIncomesNav.vue'
import ActionsMenu from '../components/ActionsMenu.vue'
import axios from '../axiosInstance'
import { Transition, ref } from 'vue'
import { useRouter } from 'vue-router';
import { checkAuthentication } from '../utils/authentication'
import { useIncomesStore } from '../stores/incomes'
import { useCardsStore } from '../stores/cards'

const router = useRouter()

if ( !checkAuthentication() ) router.replace('/login')

const incomesStore = useIncomesStore()
const cardsStore = useCardsStore()

const selectedIncomeId = ref(null)
const showActionsMenu = ref(false)

const selectIncome = (incomeId) => {
    selectedIncomeId.value = incomeId
}

const setShowActionsMenu = (value, incomeId) => {
    selectIncome(incomeId)
    showActionsMenu.value = value
}

const deleteIncomeAction = async () => {
    const response = confirm('Are you sure?')

    if (!response) return

    const token = JSON.parse( localStorage.getItem('tokenData') ).token

    try {
        await axios.delete(`/incomes/${selectedIncomeId.value}`, {
            headers: { Authorization: `Bearer ${token}` }
        })

        cardsStore.loadCards(true)
        incomesStore.loadIncomes(true)
    } catch (err) {
        switch (+err.response.status) {
            case 400:
                alert("Card amount can't be negative")
                break
        }
    } finally {
        setShowActionsMenu(false)
    }
}
</script>

<template>
    <main class="incomes_list_page">
        <IncomesList :showForm="setShowActionsMenu" />
    </main>
    <CostsIncomesNav now="incomes" />
    <Transition name="popup_form">
        <ActionsMenu v-if="showActionsMenu" :showForm="setShowActionsMenu" :deleteAction="deleteIncomeAction" />
    </Transition>
    <Navigation />
</template>

<style>
.incomes_list_page {
    padding-bottom: 200px;
}
</style>