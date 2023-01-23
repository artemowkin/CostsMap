<script setup lang="ts">
import type { RegistrationData } from '@/interfaces/auth'
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Form, Field, ErrorMessage } from 'vee-validate'
import { useUserStore } from '@/stores/user'
import { registrate } from '@/api/auth'
import * as yup from 'yup'

const userStore = useUserStore()

const router = useRouter()

const formError = ref<string | null>(null)

const registrationData = reactive<RegistrationData>({
  email: '',
  password1: '',
  password2: '',
  currency: ''
})

const schema = yup.object({
  email: yup.string().required().email(),
  password1: yup.string().required().min(8),
  password2: yup.string().required().when(['password1'], (password1, schema) => {
    return schema.oneOf([password1], 'passwords do not match')
  }),
})

const onSubmit = async () => {
    const tokenPair = await registrate(registrationData, msg => formError.value = msg)
    await userStore.setTokens(tokenPair)
    router.push({ name: 'categories' })
}
</script>

<template>
  <div class="registration_form__container">
    <Form @submit="onSubmit" :validation-schema="schema">
      <h3>Registration</h3>
      <div v-if="formError" class="form_error">{{ formError }}</div>
      <div class="input_field">
        <Field name="email" v-model="registrationData.email" placeholder="email" />
        <ErrorMessage name="email" />
      </div>

      <div class="input_field">
        <Field name="password1" type="password" v-model="registrationData.password1" placeholder="password" />
        <ErrorMessage name="password1" />
      </div>

      <div class="input_field">
        <Field name="password2" type="password" v-model="registrationData.password2" placeholder="repeat password" />
        <ErrorMessage name="password2" />
      </div>

      <select v-model="registrationData.currency">
        <option value="" disabled>Currency</option>
        <option value="$">$</option>
        <option value="₽">₽</option>
      </select>

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