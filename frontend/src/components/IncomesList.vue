<script setup>
import { useIncomesStore } from '../stores/incomes'
import { useUserStore } from '../stores/user'

const incomesStore = useIncomesStore()
const userStore = useUserStore()

incomesStore.loadIncomes()
userStore.loadUser()

const toLocaleDate = (dateString) => {
    const dateObj = new Date(dateString)

    return dateObj.toDateString()
}
</script>

<template>
    <div class="incomes_container">
        <div class="dated_incomes_container" v-for="(dateIncomes, date) in incomesStore.datedIncomes" :key="date">
            <div class="income_date_and_total">
                <div class="income_date_value">{{ toLocaleDate(date) }}</div>
                <div class="income_date_total">+ {{ dateIncomes.total }}{{ userStore.user.currency }}</div>
            </div>
            <div class="income_item" v-for="income in dateIncomes.incomes" :key="income.id">
                <div class="income_card_image" :style="{ backgroundColor: income.card.color }"></div>
                <h3 class="income_card_title">{{ income.card.title }}</h3>
                <div class="income_amount">+ {{ income.userCurrencyAmount }}{{ userStore.user.currency }}</div>
            </div>
        </div>
    </div>
</template>

<style>
.incomes_container {
    display: grid;
    gap: 1em;
}

.dated_incomes_container {
    display: grid;
    gap: 1em;
}

.income_date_and_total {
    display: flex;
    justify-content: space-between;
}

.income_item {
    display: grid;
    grid-template-columns: 50px 1fr 60px;
    gap: 1em;
    background-color: var(--background-black);
    padding: 1em;
    border-radius: 10px;
}

.income_card_image {
    width: 50px;
    height: 50px;
    border-radius: 100px;
    display: grid;
    place-items: center;
    font-size: var(--header2-text-size);
    opacity: .7;
}

.income_card_title {
    display: flex;
    justify-content: flex-start;
    align-items: center;
}

.income_amount {
    display: flex;
    justify-content: flex-end;
    align-items: center;
}
</style>
