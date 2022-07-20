<script setup>
import { Suspense } from 'vue'
import RegistrationForm from '@/components/RegistrationForm.vue'
</script>

<template>
    <main class="registration_view">
        <Suspense>
            <RegistrationForm />
        </Suspense>
    </main>
</template>

<style>
.registration_view {
    position: fixed;
    left: 0;
    top: 0;
    right: 0;
    bottom: 0;
    display: grid;
    place-content: center;
}
</style>