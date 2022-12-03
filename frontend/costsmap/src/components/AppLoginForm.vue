<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'
import { apiFetch } from '@/globals';
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const router = useRouter()

const formError = ref<string | null>(null)

const schema = yup.object({
  username: yup.string().required().min(5),
  password: yup.string().required().min(8),
})

interface LoginData {
  username: string
  password: string
}

const loginData = reactive<LoginData>({
  username: '',
  password: '',
})

const onSubmit = async () => {
  try {
    const response = await apiFetch('/api/auth/login', {
      body: loginData,
      method: 'POST'
    })
    await userStore.setTokens(response)
    router.push({ name: 'categories' })
  } catch (err) {
    switch (err?.response?.status) {
      case 422:
        formError.value = "Incorrect input"
        break
      case 401:
        formError.value = "Incorrect username or password"
        break
      default:
        formError.value = "Server error"
        break
    }
  }
}
</script>

<template>
  <div class="login_form__container">
    <Form @submit="onSubmit" :validation-schema="schema">
      <h3>Log In</h3>
      <div v-if="formError" class="form_error">{{ formError }}</div>
      <div class="input_field">
        <Field name="username" v-model="loginData.username" placeholder="username" />
        <ErrorMessage name="username" />
      </div>

      <div class="input_field">
        <Field name="password" type="password" v-model="loginData.password" placeholder="password" />
        <ErrorMessage name="password" />
      </div>

      <button type="submit">Log In</button>

      <div class="registration_link">
        or <RouterLink :to="{ name: 'registration' }">registration</RouterLink>
      </div>
    </Form>
  </div>
</template>

<style lang="scss" scoped>
.login_form__container {
  @include authenticationForm();
}
</style>