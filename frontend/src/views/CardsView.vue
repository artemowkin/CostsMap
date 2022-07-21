<script setup>
import CardsList from '../components/CardsList.vue'
import Navigation from '../components/Navigation.vue'
import { useRouter } from 'vue-router';
import { checkAuthentication } from '../utils/authentication'

const router = useRouter()

if ( !checkAuthentication() ) router.replace('/login')
</script>

<template>
    <main>
        <CardsList />
    </main>
    <Navigation />
</template>