<script setup>
import { useCostsStore } from '../stores/costs'
import { useUserStore } from '../stores/user'

const costsStore = useCostsStore()
const userStore = useUserStore()

costsStore.loadMonthCosts()
</script>

<template>
    <header class="total_info_container">
        <h3>Month costs: {{ costsStore.monthCosts }}{{ userStore.user.currency }}</h3>
        <p>Month incomes: 0{{ userStore.user.currency }}</p>
    </header>
</template>

<style>
.total_info_container {
    display: grid;
    place-items: center;
    padding: 2em 0;
    gap: .5em;
}
</style>