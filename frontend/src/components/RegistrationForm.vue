<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/axiosInstance.js'

const router = useRouter()

const getCurrencies = async () => {
    const response = await axios.get('/auth/currencies/')
    return response.data.currencies
}

const currencies = await getCurrencies()

const isEmailValid = ref(false)
const email = ref("")
const isPassword1Valid = ref(false)
const isPassword2Valid = ref(false)
const password1 = ref("")
const password2 = ref("")
const showError = ref(false)
const selectedCurrency = ref(currencies[0])

const emailInput = (el) => {
    const validRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/
    email.value = el.target.value

    if (email.value.match(validRegex))
        isEmailValid.value = true
    else
        isEmailValid.value = false
}

const password1Input = (el) => {
    const validRegex = /^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{6,}$/
    password1.value = el.target.value

    if (password1.value.match(validRegex))
        isPassword1Valid.value = true
    else
        isPassword1Valid.value = false
}

const password2Input = (el) => {
    password2.value = el.target.value

    if (password2.value === password1.value)
        isPassword2Valid.value = true
    else
        isPassword2Valid.value = false
}

const submitClass = computed(() => {
    const isFormCompleted = isEmailValid.value && isPassword1Valid.value && isPassword2Valid.value
    return isFormCompleted ? 'completed_submit_button' : ''
})

const errorMessageStyles = computed(() => {
    return showError.value ? {display: 'block'} : {display: 'none'}
})

const sendRegistration = async () => {
    if ( !isEmailValid.value || !isPassword1Valid.value || !isPassword2Valid.value ) return

    try {
        const response = await axios.post('/auth/registration/', {
            email: email.value,
            password1: password1.value,
            password2: password2.value,
            currency: selectedCurrency.value
        })
        localStorage.setItem('tokenData', JSON.stringify(response.data))
        router.push('/categories')
    } catch (err) {
        showError.value = true;
    }
}
</script>

<template>
    <form @submit.prevent="sendRegistration">
        <h2>Registration</h2>
        <div class="error_message" :style="errorMessageStyles">User with this email already exists</div>
        <input
            type="email"
            placeholder="email"
            autofocus
            @input="emailInput"
            @click="showError = false"
            :style="!isEmailValid && email ? { borderColor: '#aa0000' } : {}"
            :value="email" />
        <input
            type="password"
            placeholder="password"
            @input="password1Input"
            @click="showError = false"
            :style="!isPassword1Valid && password1 ? { borderColor: '#aa0000' } : {}"
            :value="password1" />
        <input
            type="password"
            placeholder="password secondary"
            @input="password2Input"
            @click="showError = false"
            :style="!isPassword2Valid && password2 ? { borderColor: '#aa0000' } : {}"
            :value="password2" />
        <select v-model="selectedCurrency">
            <option v-for="currency in currencies" :value="currency">{{ currency }}</option>
        </select>
        <button :class="submitClass" type="submit">Registration</button>
    </form>
</template>