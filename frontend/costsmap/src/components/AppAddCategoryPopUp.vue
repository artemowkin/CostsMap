<script setup lang="ts">
import { Form, Field, ErrorMessage } from 'vee-validate'
import { reactive, ref } from 'vue';
import * as yup from 'yup'
import { apiFetch } from '@/globals'
import { useUserStore } from '@/stores/user'
import { getRandomColor } from '@/utils'
import { useCategoriesStore } from '@/stores/categories';

interface Emits {
  (e: 'close'): void
}

interface CategoryData {
  title: string
  limit: number | null
  color: string
}

const emits = defineEmits<Emits>()

const userStore = useUserStore()
const categoriesStore = useCategoriesStore()

const schema = yup.object({
  title: yup.string().required().max(20),
  limit: yup.number().max(1_000_000),
})

const formError = ref<string | null>(null)

const categoryData = reactive<CategoryData>({
  title: '',
  limit: null,
  color: getRandomColor()
})

const onSubmit = async () => {
  try {
    await apiFetch('/api/categories/', {
      headers: { Authorization: `Bearer ${userStore.accessToken}` },
      body: categoryData,
      method: 'POST'
    })
    await categoriesStore.load()
    emits('close')
  } catch (err) {
    switch (err?.response?.status) {
      case 401:
      case 403:
        await userStore.refresh()
        await onSubmit()
        break
      case 406:
        formError.value = 'Category with this title already exists'
        break
      default:
        formError.value = 'Server error'
        break
    }
  }
}
</script>

<template>
  <div class="add_category_popup">
    <div class="popup_background" @click="emits('close')"></div>
    <Form class="popup_content" @submit="onSubmit" :validation-schema="schema">
      <h3>New Category</h3>
      <div v-if="formError" class="form_error">{{ formError }}</div>
      <div class="input_field">
        <Field name="title" placeholder="title" v-model="categoryData.title" />
        <ErrorMessage name="title" />
      </div>
      <div class="input_field">
        <Field name="limit" type="number" placeholder="limit" v-model="categoryData.limit" />
        <ErrorMessage name="limit" />
      </div>
      <div class="input_field color_field">
        <input type="color" v-model="categoryData.color" />
        <div>Color</div>
      </div>
      <button type="submit">Create</button>
    </Form>
  </div>
</template>

<style lang="scss" scoped>
.add_category_popup {
  @include popup();

  .color_field {
    display: flex;
    justify-content: center;
    align-items: center;
  }
}
</style>