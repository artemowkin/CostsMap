<script setup>
import { RouterLink } from 'vue-router'

const props = defineProps(['to'])
</script>

<template>
    <RouterLink :to="props.to" class="edit_categories_button"></RouterLink>
</template>

<style>
.edit_categories_button {
    position: fixed;
    top: 2em;
    right: 1em;
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background-color: var(--background-black);
    cursor: pointer;
}
</style>