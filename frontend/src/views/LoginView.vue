<script setup>
import LoginForm from '@/components/LoginForm.vue'
</script>

<template>
    <main class="login_view">
        <LoginForm />
    </main>
</template>

<style>
.login_view {
    position: fixed;
    left: 0;
    top: 0;
    right: 0;
    bottom: 0;
    display: grid;
    place-content: center;
}
</style>