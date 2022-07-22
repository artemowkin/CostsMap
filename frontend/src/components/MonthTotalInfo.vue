<script setup>
import { useCostsStore } from '../stores/costs'
import { useIncomesStore } from '../stores/incomes'
import { useUserStore } from '../stores/user'

const costsStore = useCostsStore()
const incomesStore = useIncomesStore()
const userStore = useUserStore()

costsStore.loadMonthCosts()
incomesStore.loadMonthIncomes()
</script>

<template>
    <header class="total_info_container">
        <h3>Month costs: {{ costsStore.monthCosts }}{{ userStore.user.currency }}</h3>
        <p>Month incomes: {{ incomesStore.monthIncomes }}{{ userStore.user.currency }}</p>
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