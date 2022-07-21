<script setup>
import { computed, defineProps, ref } from 'vue'
import { useCategoriesStore } from '../stores/categories'
import { useCardsStore } from '../stores/cards'
import { dateToLocalizedISO } from '../utils/time'
import axios from '../axiosInstance'
import { useCostsStore } from '../stores/costs'

const cardsStore = useCardsStore()
const categoriesStore = useCategoriesStore()
const costsStore = useCostsStore()

const props = defineProps(['categoryId', 'setShowAddCosts'])

const card = ref(cardsStore.cards[0].id)
const date = ref( dateToLocalizedISO(new Date()) )
const userCurrencyAmount = ref("")
const isUserCurrencyAmountValid = ref(false)
const showError = ref(false)

const currentCategory = computed(() => {
    return categoriesStore.categories.find((category) => category.id === props.categoryId) ?? {}
})

const userCurrencyAmountInput = (el) => {
    const elementValue = el.target.value

    userCurrencyAmount.value = elementValue

    const selectedCard = cardsStore.cards.find((cardEl) => +card.value === cardEl.id)

    if(!isNaN(elementValue) && elementValue > 0 && elementValue <= selectedCard.amount) {
        isUserCurrencyAmountValid.value = true
    } else {
        isUserCurrencyAmountValid.value = false
    }
}

const submitClass = computed(() => {
    const isFormCompleted = isUserCurrencyAmountValid.value
    return isFormCompleted ? 'completed_submit_button' : ''
})

const sendCreateCost = async () => {
    if (!isUserCurrencyAmountValid.value) return

    const requestData = {
        userCurrencyAmount: +userCurrencyAmount.value,
        date: date.value,
        cardId: +card.value,
        categoryId: currentCategory.value.id
    }

    const token = JSON.parse( localStorage.getItem('tokenData') ).token

    try {
        await axios.post('/costs/', requestData, {
            headers: { Authorization: `Bearer ${token}` }
        })

        cardsStore.loadCards(true)
        categoriesStore.loadCategories(true)
        costsStore.loadCosts(true)
        costsStore.loadMonthCosts()

        props.setShowAddCosts(false)
    } catch (err) {
        showError.value = true
    }
}
</script>

<template>
    <div class="popup_form_container">
        <div class="close_div" @click="setShowAddCosts(false)"></div>
        <form @submit.prevent="sendCreateCost">
            <h2>New "{{ currentCategory.title }}" cost</h2>
            <div class="error_message" :style="showError ? { display: 'block' } : { display: 'none' }">Error with sending request</div>
            <select v-model="card" @click="showError = false">
                <option v-for="card in cardsStore.cards" :value="card.id">{{ card.title }}</option>
            </select>
            <input
                inputmode="decimal"
                placeholder="Cost Amount"
                @click="showError = false"
                @input="userCurrencyAmountInput"
                :value="userCurrencyAmount"
                :style="!isUserCurrencyAmountValid && userCurrencyAmount ? { borderColor: '#aa0000' } : {}"
                required />
            <input type="date" v-model="date" @click="showError = false" />
            <button :class="submitClass" type="submit">Add Cost</button>
        </form>
    </div>
</template>