<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <nav class="navigation_container">
    <RouterLink to="/" class="navigation_container__item">
      <img src="@/assets/icons/categories.svg" class="navigation_container__item_icon" />
      <div class="navigation_container__item_title">categories</div>
    </RouterLink>
    <RouterLink to="/" class="navigation_container__item">
      <img src="@/assets/icons/cards.svg" class="navigation_container__item_icon" />
      <div class="navigation_container__item_title">cards</div>
    </RouterLink>
    <RouterLink to="/" class="navigation_container__item">
      <img src="@/assets/icons/costs.svg" class="navigation_container__item_icon" />
      <div class="navigation_container__item_title">costs</div>
    </RouterLink>
    <RouterLink to="/" class="navigation_container__item">
      <img src="@/assets/icons/statistic.svg" class="navigation_container__item_icon" />
      <div class="navigation_container__item_title">statistic</div>
    </RouterLink>
    <RouterLink to="/" class="navigation_container__item">
      <img src="@/assets/icons/account.svg" class="navigation_container__item_icon" />
      <div class="navigation_container__item_title">account</div>
    </RouterLink>
  </nav>
</template>

<style lang="scss" scoped>
.navigation_container {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: $navigation-background;
  padding: 1rem;
  display: grid;
  grid-template-columns: repeat(5, minmax(60px, 1fr));
  place-content: center space-evenly;
  gap: .5rem;
  backdrop-filter: blur(20px);
  z-index: 100;

  .navigation_container__item {
    display: grid;
    place-items: center;
    gap: .25rem;
    -webkit-tap-highlight-color: transparent;

    .navigation_container__item_icon {
      width: 80%;
      aspect-ratio: 1 / 1;
      border-radius: 1rem;
      background-color: $navigation-icon-background;
      object-fit: contain;
      padding: .75rem;
    }

    .navigation_container__item_title {
      color: $navigation-text-color;
      font-size: .5rem;
    }
  }
}
</style>