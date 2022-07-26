<script setup>
import { useCardsStore } from '../stores/cards'

const props = defineProps(['showForm'])

const cardsStore = useCardsStore()

cardsStore.loadCards()
</script>

<template>
    <div class="cards_container">
        <div v-for="card in cardsStore.cards" class="card_item" :key="card.id" @click="props.showForm(true, card.id)">
            <div class="card_icon" :style="{ backgroundColor: card.color }"></div>
            <div class="card_info_block">
                <h2 class="card_title">{{ card.title }}</h2>
                <div class="card_amount">{{ card.amount }}{{ card.currency }}</div>
            </div>
        </div>
    </div>
</template>

<style>
.cards_container {
    display: grid;
    gap: 1em;
}

.card_item {
    width: 100%;
    background-color: var(--background-black);
    padding: 1em;
    border-radius: 10px;
    display: grid;
    place-items: center start;
    grid-template-columns: repeat(2, min-content);
    gap: 1em;
    cursor: pointer;
}

.card_icon {
    width: 60px;
    height: 60px;
    border-radius: 100px;
    opacity: .6;
}

.card_info_block {
    display: grid;
    gap: .5em;
}
</style>
