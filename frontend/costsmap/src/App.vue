<script setup lang="ts">
import { RouterView } from 'vue-router'
import AppNavigation from '@/components/AppNavigation.vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
</script>

<template>
  <RouterView />
  <AppNavigation v-if="userStore.currentUser" />
</template>

<style lang="scss" scoped>
@import '@/styles/main.scss';
</style>
