<script setup>
import { computed, ref } from 'vue'
import { useCardsStore } from '../stores/cards'
import { useUserStore } from '../stores/user'
import axios from '../axiosInstance'

const cardsStore = useCardsStore()
const userStore = useUserStore()

const props = defineProps(['setShowAddCard'])

const currencies = ref([])
const title = ref("")
const currency = ref("")
const color = ref("#000000")
const isTitleValid = ref(false)
const showError = ref(false)

const getCurrencies = async () => {
    const response = await axios.get('/auth/currencies/')
    return response.data.currencies
}

userStore.loadUser().then(() => currency.value = userStore.user.currency)

getCurrencies().then((responseCurrencies) => currencies.value = responseCurrencies)

const titleInput = (el) => {
    const elementValue = el.target.value

    title.value = elementValue

    if(elementValue.length > 0 && elementValue.length <= 15) {
        isTitleValid.value = true
    } else {
        isTitleValid.value = false
    }
}

const submitClass = computed(() => {
    const isFormCompleted = isTitleValid.value
    return isFormCompleted ? 'completed_submit_button' : ''
})

const sendCreateCard = async () => {
    if (!isTitleValid.value) return

    const requestData = {
        title: title.value,
        currency: currency.value,
        color: color.value
    }

    const token = JSON.parse( localStorage.getItem('tokenData') ).token

    try {
        await axios.post('/cards/', requestData, {
            headers: { Authorization: `Bearer ${token}` }
        })

        cardsStore.loadCards(true)

        props.setShowAddCard(false)
    } catch (err) {
        showError.value = true
    }
}
</script>

<template>
    <div class="popup_form_container">
        <div class="close_div" @click="props.setShowAddCard(false)"></div>
        <form @submit.prevent="sendCreateCard">
            <h2>New card</h2>
            <div class="error_message" :style="showError ? { display: 'block' } : { display: 'none' }">Error with sending request</div>
            <input
                type="text"
                placeholder="Card Title"
                @click="showError = false"
                @input="titleInput"
                :value="title"
                :style="!isTitleValid && title ? { borderColor: '#aa0000' } : {}"
                required />
            <select v-model="currency" @click="showError = false">
                <option v-for="currencyEl in currencies" :value="currencyEl">{{ currencyEl }}</option>
            </select>
            <input type="color" v-model="color" @click="showError = false" />
            <button :class="submitClass" type="submit">Add Card</button>
        </form>
    </div>
</template>