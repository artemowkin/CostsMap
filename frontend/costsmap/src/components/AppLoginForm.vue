<script setup lang="ts">
import type { LoginData } from '@/interfaces/auth'
import { login } from '@/api/auth'
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const router = useRouter()

const formError = ref<string | null>(null)

const schema = yup.object({
  email: yup.string().required().email(),
  password: yup.string().required(),
})

const loginData = reactive<LoginData>({
  email: '',
  password: '',
})

const onSubmit = async () => {
  const tokenPair = await login(loginData, (msg) => formError.value = msg)
  await userStore.setTokens(tokenPair)
  console.log('redirecting on categories')
  router.push({ name: 'categories' })
}
</script>

<template>
  <div class="login_form__container">
    <Form @submit="onSubmit" :validation-schema="schema">
      <h3>Log In</h3>
      <div v-if="formError" class="form_error">{{ formError }}</div>
      <div class="input_field">
        <Field name="email" v-model="loginData.email" placeholder="email" />
        <ErrorMessage name="email" />
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