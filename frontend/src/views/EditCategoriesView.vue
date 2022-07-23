<script setup>
import CategoriesList from '@/components/CategoriesList.vue'
import Navigation from '@/components/Navigation.vue'
import EditCategoriesButton from '@/components/EditCategoriesButton.vue'
import AddCategoryForm from '@/components/AddCategoryForm.vue'
import { ref, Transition } from 'vue'
import { useRouter } from 'vue-router';
import { checkAuthentication } from '../utils/authentication'

const router = useRouter()

const showAddCategoryForm = ref(false)

const setShowForm = (value) => {
    showAddCategoryForm.value = value
}

if ( !checkAuthentication() ) router.replace('/login')
</script>

<template>
    <header class="edit_header">
        <h3>Edit Categories</h3>
    </header>
    <EditCategoriesButton to="/categories" />
    <main>
        <CategoriesList :withAddButton="true" :setShowForm="setShowForm" />
    </main>
    <Navigation />
    <Transition name="popup_form">
        <AddCategoryForm v-if="showAddCategoryForm" :setShowForm="setShowForm" />
    </Transition>
</template>

<style>
.edit_header {
    display: grid;
    place-items: center;
    padding: 2.75em 0;
}
</style>