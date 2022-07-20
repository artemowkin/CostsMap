<script setup>
import CategoriesList from '@/components/CategoriesList.vue'
import Navigation from '@/components/Navigation.vue';
import { useRouter } from 'vue-router';
import MonthTotalInfo from '../components/MonthTotalInfo.vue'
import { checkAuthentication } from '../utils/authentication'

const router = useRouter()

if ( !checkAuthentication() ) router.replace('/login')
</script>

<template>
    <MonthTotalInfo />
    <main>
        <CategoriesList />
    </main>
    <Navigation />
</template>