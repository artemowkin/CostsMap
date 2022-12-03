<script setup lang="ts">
import type { Category } from '@/stores/categories'
import { useUserStore } from '@/stores/user'
import { computed } from 'vue'

interface Props {
  category: Category
}

const props = defineProps<Props>()

interface Emits {
  (e: 'click', category: Category): void
}

const emits = defineEmits<Emits>()

const userStore = useUserStore()

const categoryStyle = computed(() => {
  return { backgroundColor: props.category.color }
})
</script>

<template>
  <div class="category" @click="emits('click', props.category)">
    <div class="category_title">{{ props.category.title }}</div>
    <div class="category_costs">0{{ userStore.currentUser!.currency }}</div>
    <div class="category_circle" :style="categoryStyle">{{ userStore.currentUser!.currency }}</div>
    <div class="category_limit">{{ props.category.limit }}{{ userStore.currentUser!.currency }}</div>
  </div>
</template>

<style lang="scss" scoped>
.category {
  display: flex;
  flex-direction: column;
  gap: .5rem;
  justify-content: flex-end;
  align-items: center;

  .category_costs, .category_limit, .category_title {
    text-align: center;
    font-size: .75rem;
  }

  .category_title {
    font-weight: 700;
    word-break: break-all;
  }

  .category_circle {
    width: 100%;
    aspect-ratio: 1 / 1;
    border-radius: 50%;
    position: relative;
    display: grid;
    place-items: center;
    font-size: 2rem;
    color: white;

    &::before {
      content: '';
      display: block;
      position: absolute;
      left: .25rem;
      top: .25rem;
      right: .25rem;
      bottom: .25rem;
      background-color: $category-transparent;
      border-radius: 50%;
    }
  }
}
</style>