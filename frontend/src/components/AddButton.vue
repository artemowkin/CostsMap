<script setup>
const props = defineProps(['showForm'])
</script>

<template>
    <button class="add_income_button" @click="props.showForm(true)">+</button>
</template>

<style>
.add_income_button {
    position: fixed;
    bottom: 120px;
    right: 1em;
    padding: 15px 25px;
    font-size: var(--header1-text-size);
    background-color: var(--blue-500);
    color: var(--background-blacker);
    display: grid;
    place-items: center;
    border-radius: 100px;
}
</style>