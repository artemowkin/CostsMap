<script setup>
import { computed, ref } from 'vue'
import { useCardsStore } from '../stores/cards'
import { dateToLocalizedISO } from '../utils/time'
import axios from '../axiosInstance'
import { useIncomesStore } from '../stores/incomes'

const cardsStore = useCardsStore()
const incomesStore = useIncomesStore()

const props = defineProps(['setShowAddIncomes'])

const card = ref(cardsStore.cards[0].id)
const date = ref( dateToLocalizedISO(new Date()) )
const userCurrencyAmount = ref("")
const isUserCurrencyAmountValid = ref(false)
const showError = ref(false)

const userCurrencyAmountInput = (el) => {
    const elementValue = el.target.value

    userCurrencyAmount.value = elementValue

    if(!isNaN(elementValue) && elementValue > 0 && elementValue < 10000000) {
        isUserCurrencyAmountValid.value = true
    } else {
        isUserCurrencyAmountValid.value = false
    }
}

const submitClass = computed(() => {
    const isFormCompleted = isUserCurrencyAmountValid.value
    return isFormCompleted ? 'completed_submit_button' : ''
})

const sendCreateIncome = async () => {
    if (!isUserCurrencyAmountValid.value) return

    const requestData = {
        userCurrencyAmount: +userCurrencyAmount.value,
        date: date.value,
        cardId: +card.value,
    }

    const token = JSON.parse( localStorage.getItem('tokenData') ).token

    try {
        await axios.post('/incomes/', requestData, {
            headers: { Authorization: `Bearer ${token}` }
        })

        cardsStore.loadCards(true)
        incomesStore.loadIncomes(true)
        incomesStore.loadMonthIncomes()

        props.setShowAddIncomes(false)
    } catch (err) {
        showError.value = true
    }
}
</script>

<template>
    <div class="popup_form_container">
        <div class="close_div" @click="setShowAddIncomes(false)"></div>
        <form @submit.prevent="sendCreateIncome">
            <h2>New income</h2>
            <div class="error_message" :style="showError ? { display: 'block' } : { display: 'none' }">Error with sending request</div>
            <select v-model="card" @click="showError = false">
                <option v-for="card in cardsStore.cards" :value="card.id">{{ card.title }}</option>
            </select>
            <input
                inputmode="decimal"
                placeholder="Income Amount"
                @click="showError = false"
                @input="userCurrencyAmountInput"
                :value="userCurrencyAmount"
                :style="!isUserCurrencyAmountValid && userCurrencyAmount ? { borderColor: '#aa0000' } : {}"
                required />
            <input type="date" v-model="date" @click="showError = false" />
            <button :class="submitClass" type="submit">Add Income</button>
        </form>
    </div>
</template>