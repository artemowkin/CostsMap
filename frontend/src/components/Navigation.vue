<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <nav class="navigation">
    <RouterLink to="/categories">
        <div class="logo_container"></div>
        <small>categories</small>
    </RouterLink>
    <RouterLink to="/cards">
        <div class="logo_container"></div>
        <small>cards</small>
    </RouterLink>
    <RouterLink to="/costs">
        <div class="logo_container"></div>
        <small>costs</small>
    </RouterLink>
    <RouterLink to="/statistic">
        <div class="logo_container"></div>
        <small>statistic</small>
    </RouterLink>
    <!-- <RouterLink to="/account">
        <div class="logo_container"></div>
        <small>account</small>
    </RouterLink> -->
  </nav>
</template>

<style>
.navigation {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 1em .5em;
  background-color: var(--background-black);
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(50px, 1fr));
  place-content: center space-evenly;
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
