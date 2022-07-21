<script setup>
import { RouterLink } from 'vue-router'
import { defineProps } from 'vue'

const props = defineProps(['now'])
</script>

<template>
    <div class="costs_incomes_links_container">
        <div class="costs_incomes_links">
            <span v-if="props.now === 'costs'">costs</span>
            <RouterLink to="/costs" v-else>costs</RouterLink>
            <span v-if="props.now === 'incomes'">incomes</span>
            <RouterLink to="/incomes" v-else>incomes</RouterLink>
        </div>
    </div>
</template>

<style>
.costs_incomes_links_container {
    position: fixed;
    left: 1em;
    right: 1em;
    bottom: 130px;
    display: grid;
    place-content: center;
}

.costs_incomes_links {
    padding: 1em 0;
    border-radius: 100px;
    background-color: var(--background-blacker);
}

.costs_incomes_links a {
    padding: 1em 2em;
    border-radius: 100px;
    background-color: var(--blue-900);
    color: var(--blue-500);
}

.costs_incomes_links span {
    padding: 1em 2em;
}
</style>