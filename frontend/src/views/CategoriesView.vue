<script setup>
import CategoriesList from '@/components/CategoriesList.vue'
import Navigation from '@/components/Navigation.vue';
import MonthTotalInfo from '../components/MonthTotalInfo.vue'
</script>

<template>
    <MonthTotalInfo />
    <main>
        <CategoriesList />
    </main>
    <Navigation />
</template>