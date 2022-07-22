<script setup>
import IncomesList from '../components/IncomesList.vue'
import Navigation from '../components/Navigation.vue'
import CostsIncomesNav from '../components/CostsIncomesNav.vue'
import { useRouter } from 'vue-router';
import { checkAuthentication } from '../utils/authentication'

const router = useRouter()

if ( !checkAuthentication() ) router.replace('/login')
</script>

<template>
    <main class="incomes_list_page">
        <IncomesList />
    </main>
    <CostsIncomesNav now="incomes" />
    <Navigation />
</template>

<style>
.incomes_list_page {
    padding-bottom: 200px;
}
</style>