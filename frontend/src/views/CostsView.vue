<script setup>
import CostsList from '../components/CostsList.vue'
import Navigation from '../components/Navigation.vue'
import CostsIncomesNav from '../components/CostsIncomesNav.vue'
import { useRouter } from 'vue-router';
import { checkAuthentication } from '../utils/authentication'

const router = useRouter()

if ( !checkAuthentication() ) router.replace('/login')
</script>

<template>
    <main class="costs_list_page">
        <CostsList />
    </main>
    <CostsIncomesNav now="costs" />
    <Navigation />
</template>

<style>
.costs_list_page {
    padding-bottom: 200px;
}
</style>
