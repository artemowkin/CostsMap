<script setup>
import { RouterLink } from 'vue-router'
import EditIcon from '../assets/icons/edit_light.svg'

const props = defineProps(['to'])
</script>

<template>
    <RouterLink :to="props.to" class="edit_categories_button">
        <img :src="EditIcon" />
    </RouterLink>
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
    display: grid;
    place-content: center;
}

.edit_categories_button img {
    width: 20px;
    height: 20px;
    opacity: .6;
}
</style>