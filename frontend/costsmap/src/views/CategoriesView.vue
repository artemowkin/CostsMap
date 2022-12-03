<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AppCategoriesList from '@/components/AppCategoriesList.vue'
import { useCategoriesStore } from '@/stores/categories'

const categoriesStore = useCategoriesStore()

const categoriesEditMode = ref<boolean>(true)

onMounted(() => {
  categoriesStore.load()
})
</script>

<template>
  <div class="categories_page">
    <AppCategoriesList
      :categories="categoriesStore.categories"
      :edit-mode="categoriesEditMode" />
  </div>
</template>

<style lang="scss" scoped>
  .categories_page {
    @include wrapper();
  }
</style>