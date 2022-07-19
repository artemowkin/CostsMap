<script setup>
import { computed, ref } from 'vue';

const isEmailValid = ref(false);
const email = ref("");
const isPasswordValid = ref(false);
const password = ref("");

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

    if (password.value.length > 0)
        isPasswordValid.value = true
    else
        isPasswordValid.value = false
}

const submitClass = computed(() => {
    const isFormCompleted = isEmailValid.value && isPasswordValid.value
    return isFormCompleted ? 'completed_submit_button' : ''
})
</script>

<template>
    <form>
        <h2>Log In</h2>
        <input
            type="email"
            placeholder="email"
            autofocus
            @input="emailInput"
            :value="email" />
        <input
            type="password"
            placeholder="password"
            @input="passwordInput"
            :value="password" />
        <button :class="submitClass" type="submit">Log In</button>
    </form>
</template>