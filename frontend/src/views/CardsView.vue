<script setup>
import CardsList from '../components/CardsList.vue'
import Navigation from '../components/Navigation.vue'
import { ref, Suspense } from 'vue'
import { useRouter } from 'vue-router'
import { checkAuthentication } from '../utils/authentication'
import AddButton from '../components/AddButton.vue'
import AddCardForm from '../components/AddCardForm.vue'

const router = useRouter()

if ( !checkAuthentication() ) router.replace('/login')

const showAddCardForm = ref(false)

const setShowAddCardForm = (value) => {
    showAddCardForm.value = value
}
</script>

<template>
    <main>
        <CardsList />
    </main>
    <AddButton :showForm="setShowAddCardForm" />
    <Transition name="popup_form">
        <Suspense>
            <AddCardForm v-if="showAddCardForm" :setShowAddCard="setShowAddCardForm" />
        </Suspense>
    </Transition>
    <Navigation />
</template>