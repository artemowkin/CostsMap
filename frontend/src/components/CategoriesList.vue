<script setup>
import { useCategoriesStore } from '../stores/categories'
import { useUserStore } from '../stores/user'
import AddCategoryButton from './AddCategoryButton.vue';

const props = defineProps(['setSelectedCategoryId', 'withAddButton', 'setShowForm'])

const categoriesStore = useCategoriesStore()

const userStore = useUserStore()

categoriesStore.loadCategories()

userStore.loadUser()
</script>

<template>
    <div class="categories_container">
        <div v-for="category in categoriesStore.categories" class="category" :key="category.id" @click="props.setSelectedCategoryId(category.id)">
            <div class="category_title">{{ category.title }}</div>
            <div class="category_costs_limit">{{ category.costsLimit || 0 }}{{ userStore.user.currency }}</div>
            <div class="category_icon" :style="{ backgroundColor: category.color }">{{ userStore.user.currency }}</div>
            <div class="category_costs_sum">{{ category.costsSum }}{{ userStore.user.currency }}</div>
        </div>
        <AddCategoryButton v-if="props.withAddButton" :setShowForm="props.setShowForm" />
    </div>
</template>

<style>
.categories_container {
    width: 100%;
    display: grid;
    grid-template-columns: repeat(4, minmax(60px, 1fr));
    gap: .5em;
}

.category {
    display: grid;
    place-items: start center;
    gap: .25em;
    cursor: pointer;
}

.category_icon {
    width: 60px;
    height: 60px;
    display: grid;
    place-content: center;
    border-radius: 100px;
    font-size: var(--header1-text-size);
    background-blend-mode: darken;
    opacity: .7;
}
</style>