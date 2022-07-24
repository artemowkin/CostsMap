<script setup>
import { useCostsStore } from '../stores/costs'
import { useUserStore } from '../stores/user'

const costsStore = useCostsStore()
const userStore = useUserStore()

costsStore.loadCosts()
userStore.loadUser()

const toLocaleDate = (dateString) => {
    const dateObj = new Date(dateString)

    return dateObj.toDateString()
}
</script>

<template>
    <div class="costs_container">
        <div class="dated_costs_container" v-for="(dateCosts, date) in costsStore.datedCosts" :key="date">
            <div class="cost_date_and_total">
                <div class="cost_date_value">{{ toLocaleDate(date) }}</div>
                <div class="cost_date_total">- {{ dateCosts.total }}{{ userStore.user.currency }}</div>
            </div>
            <div class="cost_item" v-for="cost in dateCosts.costs" :key="cost.id">
                <div class="cost_category_image" :style="{ backgroundColor: cost.category.color }">{{ userStore.user.currency }}</div>
                <div class="cost_info">
                    <h3 class="cost_category_title">{{ cost.category.title }}</h3>
                    <div class="cost_card_title">{{ cost.card.title }}</div>
                </div>
                <div class="cost_amount">- {{ cost.userCurrencyAmount }}{{ userStore.user.currency }}</div>
            </div>
        </div>
    </div>
</template>

<style>
.costs_container {
    display: grid;
    gap: 1em;
}

.dated_costs_container {
    display: grid;
    gap: 1em;
}

.cost_date_and_total {
    display: flex;
    justify-content: space-between;
}

.cost_item {
    display: grid;
    grid-template-columns: 50px 1fr 100px;
    gap: 1em;
    background-color: var(--background-black);
    padding: 1em;
    border-radius: 10px;
}

.cost_category_image {
    width: 50px;
    height: 50px;
    border-radius: 100px;
    display: grid;
    place-items: center;
    font-size: var(--header2-text-size);
    opacity: .7;
}

.cost_info {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: .25em;
}

.cost_amount {
    display: flex;
    justify-content: flex-end;
    align-items: center;
}
</style>
