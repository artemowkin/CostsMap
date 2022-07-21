<script setup>
import CategoriesList from '@/components/CategoriesList.vue'
import Navigation from '@/components/Navigation.vue'
import AddCostForm from '@/components/AddCostForm.vue'
import { ref, Transition } from 'vue'
import { useRouter } from 'vue-router';
import MonthTotalInfo from '../components/MonthTotalInfo.vue'
import { checkAuthentication } from '../utils/authentication'
import { useCardsStore } from '../stores/cards'

const router = useRouter()

if ( !checkAuthentication() ) router.replace('/login')

const cardsStore = useCardsStore()
cardsStore.loadCards()

const selectedCategoryId = ref(null)
const showAddCosts = ref(false)

const setShowAddCosts = (value) => {
    if (cardsStore.cards.length === 0) return

    showAddCosts.value = value
}

const setSelectedCategoryId = (categoryId) => {
    selectedCategoryId.value = categoryId
    setShowAddCosts(true)
}
</script>

<template>
    <MonthTotalInfo />
    <main>
        <CategoriesList :setSelectedCategoryId="setSelectedCategoryId" />
    </main>
    <Navigation />
    <Transition name="popup_form">
        <AddCostForm v-if="showAddCosts" :categoryId="selectedCategoryId" :setShowAddCosts="setShowAddCosts" />
    </Transition>
</template>