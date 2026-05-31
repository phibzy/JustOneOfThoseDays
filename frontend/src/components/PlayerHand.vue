<script setup lang="ts">
import type { CardInfo } from '../types/game'

defineProps<{
  cards: CardInfo[]
  title?: string
}>()
</script>

<template>
  <div class="panel">
    <div class="panel-header">
      <h3>{{ title || 'Your Hand' }}</h3>
    </div>
    <div v-if="cards.length === 0" style="color: var(--text-muted); text-align: center; padding: 16px;">
      No cards yet
    </div>
    <div v-else class="hand-cards">
      <div
        v-for="(card, index) in cards"
        :key="index"
        class="game-card-mini"
      >
        <span class="card-mini-desc">{{ card.desc }}</span>
        <span class="card-mini-value">{{ card.value }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.hand-cards {
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-height: 400px;
  overflow-y: auto;
}
</style>
