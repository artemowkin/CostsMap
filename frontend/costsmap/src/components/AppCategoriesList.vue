<script setup lang="ts">
import { ref } from 'vue'
import type { Category } from '@/stores/categories'
import AppCategoriesListItem from '@/components/AppCategoriesListItem.vue'
import AppAddCategoryPopUp from '@/components/AppAddCategoryPopUp.vue'

interface Props {
  categories: Category[]
  editMode: boolean
}

const props = defineProps<Props>()

const showAddPopUp = ref<boolean>(false)

const onCategoryClick = (category: Category) => {
  if (!props.editMode) return
}

const onAddClick = () => {
  showAddPopUp.value = true
}

const onAddClose = () => {
  showAddPopUp.value = false
}
</script>

<template>
  <AppAddCategoryPopUp v-if="showAddPopUp" @close="onAddClose" />
  <div class="categories_list">
    <AppCategoriesListItem
      v-for="category in props.categories"
      :category="category"
      :key="category.uuid"
      @click="onCategoryClick"
    />
    <div v-if="props.editMode" class="categories_list__add_button" @click="onAddClick">
      <div class="categories_list__add_button_icon">+</div>
      <div class="categories_list__add_button_title">Add</div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.categories_list {
  display: grid;
  grid-template-columns: repeat(4, minmax(60px, 1fr));
  gap: 1rem;

  .categories_list__add_button {
    display: grid;
    gap: .5rem;
    place-content: end center;
    place-items: center;
    grid-template-columns: 1fr;

    .categories_list__add_button_icon {
      width: 100%;
      aspect-ratio: 1 / 1;
      background-color: $add-category-icon-background;
      border-radius: 50%;
      display: grid;
      place-items: center;
      font-size: 2rem;
      color: $add-category-plus-color;
    }

    .categories_list__add_button_title {
      font-size: .75rem;
    }
  }
}
</style>