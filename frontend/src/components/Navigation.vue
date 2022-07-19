<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <nav class="navigation">
    <RouterLink to="/login">
        <div class="logo_container"></div>
        <small>categories</small>
    </RouterLink>
    <RouterLink to="/login">
        <div class="logo_container"></div>
        <small>cards</small>
    </RouterLink>
    <RouterLink to="/login">
        <div class="logo_container"></div>
        <small>costs</small>
    </RouterLink>
    <RouterLink to="/login">
        <div class="logo_container"></div>
        <small>statistic</small>
    </RouterLink>
    <RouterLink to="/login">
        <div class="logo_container"></div>
        <small>account</small>
    </RouterLink>
  </nav>
</template>

<style>
.navigation {
  position: fixed;
  bottom: 1em;
  left: 1em;
  right: 1em;
  padding: 1em .5em;
  border-radius: 20px;
  background-color: var(--background-black);
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  place-content: center space-between;
  place-items: center;
  z-index: 1000;
}

.navigation a {
  display: grid;
  place-content: center;
  place-items: center;
}

.logo_container {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  background-color: var(--orange-800);
}
</style>
