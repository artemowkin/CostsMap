<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Form, Field, ErrorMessage } from 'vee-validate'
import { useUserStore } from '@/stores/user'
import { apiFetch } from '@/globals'
import * as yup from 'yup'

interface RegistrationData {
  username: string
  password1: string
  password2: string
  currency?: string
  language?: string
}

const userStore = useUserStore()

const router = useRouter()

const formError = ref<string | null>(null)

const registrationData = reactive<RegistrationData>({
  username: '',
  password1: '',
  password2: '',
})

const schema = yup.object({
  username: yup.string().required().min(5),
  password1: yup.string().required().min(8),
  password2: yup.string().required().when(['password1'], (password1, schema) => {
    return schema.oneOf([password1], 'passwords do not match')
  }),
})

const onSubmit = async () => {
  try {
    const response = await apiFetch('/api/auth/registration', {
      body: registrationData,
      method: 'POST'
    })

    await userStore.setTokens(response)
    router.push({ name: 'categories' })
  } catch (err) {
    switch (err?.response?.status) {
      case 422:
        formError.value = 'Incorrect input'
        break
      case 400:
        formError.value = 'User with this username already exists'
        break
      case 401:
        formError.value = 'Incorrect username or password'
        break
      default:
        formError.value = 'Server error'
        break
    }
  }
}
</script>

<template>
  <div class="registration_form__container">
    <Form @submit="onSubmit" :validation-schema="schema">
      <h3>Registration</h3>
      <div v-if="formError" class="form_error">{{ formError }}</div>
      <div class="input_field">
        <Field name="username" v-model="registrationData.username" placeholder="username" />
        <ErrorMessage name="username" />
      </div>

      <div class="input_field">
        <Field name="password1" type="password" v-model="registrationData.password1" placeholder="password" />
        <ErrorMessage name="password1" />
      </div>

      <div class="input_field">
        <Field name="password2" type="password" v-model="registrationData.password2" placeholder="repeat password" />
        <ErrorMessage name="password2" />
      </div>

      <button type="submit">Registration</button>

      <div class="registration_link">
        or <RouterLink :to="'/'">log in</RouterLink>
      </div>
    </Form>
  </div>
</template>

<style lang="scss" scoped>
.registration_form__container {
  @include authenticationForm();
}
</style>