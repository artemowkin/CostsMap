<script setup>
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from '@/axiosInstance.js'

const router = useRouter();

const isEmailValid = ref(false);
const email = ref("");
const isPasswordValid = ref(false);
const password = ref("");
const showError = ref(false)

const emailInput = (el) => {
    const validRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/
    email.value = el.target.value

    if (email.value.match(validRegex))
        isEmailValid.value = true
    else
        isEmailValid.value = false
}

const passwordInput = (el) => {
    password.value = el.target.value

    if (password.value.length >= 6)
        isPasswordValid.value = true
    else
        isPasswordValid.value = false
}

const submitClass = computed(() => {
    const isFormCompleted = isEmailValid.value && isPasswordValid.value
    return isFormCompleted ? 'completed_submit_button' : ''
})

const errorMessageStyles = computed(() => {
    return showError.value ? {display: 'block'} : {display: 'none'}
})

const sendLogIn = async () => {
    if ( !isEmailValid.value || !isPasswordValid.value ) return

    try {
        const response = await axios.post('/auth/login/', {
            email: email.value, password: password.value
        })
        localStorage.setItem('tokenData', JSON.stringify(response.data))
        router.push('/categories')
    } catch (err) {
        showError.value = true;
    }
}
</script>

<template>
    <form @submit.prevent="sendLogIn">
        <h2>Log In</h2>
        <div class="error_message" :style="errorMessageStyles">Incorrect email or password</div>
        <input
            type="email"
            placeholder="email"
            autofocus
            @input="emailInput"
            @click="showError = false"
            :value="email" />
        <input
            type="password"
            placeholder="password"
            @input="passwordInput"
            @click="showError = false"
            :value="password" />
        <button :class="submitClass" type="submit">Log In</button>
    </form>
</template>