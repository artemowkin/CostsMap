<script setup>
import { Suspense } from 'vue'
import RegistrationForm from '@/components/RegistrationForm.vue'
</script>

<template>
    <main>
        <Suspense>
            <RegistrationForm />
        </Suspense>
    </main>
</template>