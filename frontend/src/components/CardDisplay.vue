<script setup lang="ts">
import { computed } from 'vue'
import type { CardInfo } from '../types/game'

const props = defineProps<{
  card: CardInfo
  showValue?: boolean
  size?: 'normal' | 'large'
}>()

const sizeClass = computed(() => props.size === 'large' ? 'game-card-large' : '')
</script>

<template>
  <div class="game-card" :class="sizeClass">
    <div class="card-label">Misery Card</div>
    <div class="card-desc">{{ card.desc }}</div>
    <div v-if="showValue && card.value !== undefined" class="card-value">
      {{ card.value }}
    </div>
    <div v-else class="card-value" style="color: var(--text-muted);">
      ???
    </div>
  </div>
</template>

<style scoped>
.game-card-large {
  padding: 32px;
}

.game-card-large .card-desc {
  font-size: 1.75rem;
}

.game-card-large .card-value {
  font-size: 2.5rem;
}
</style>
