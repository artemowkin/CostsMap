<script setup>
const props = defineProps(['setShowForm'])
</script>

<template>
    <div class="category" @click="props.setShowForm(true)">
        <p>Add</p>
        <div class="category_icon add_icon">+</div>
    </div>
</template>

<style>
.add_icon {
    opacity: 1 !important;
    background-color: var(--blue-900);
    color: var(--blue-500);
}
</style>