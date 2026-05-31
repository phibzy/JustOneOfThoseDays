<script setup lang="ts">
import type { RangeOption, RangeInfo } from '../types/game'

const props = defineProps<{
  ranges: RangeOption[]
  previousGuesses: RangeInfo[]
  disabled: boolean
}>()

const emit = defineEmits<{
  (e: 'select', index: number): void
}>()

function isGuessedWrong(range: RangeOption): boolean {
  return props.previousGuesses.some(
    (g) => g.low === range.low && g.high === range.high
  )
}

function handleSelect(range: RangeOption) {
  if (!props.disabled && !isGuessedWrong(range)) {
    emit('select', range.index - 1)
  }
}
</script>

<template>
  <div class="panel">
    <div class="panel-header">
      <h3>Choose a Range</h3>
    </div>
    <div class="range-list">
      <button
        v-for="range in ranges"
        :key="range.index"
        class="range-btn"
        :class="{ 'guessed-wrong': isGuessedWrong(range) }"
        :disabled="disabled || isGuessedWrong(range)"
        @click="handleSelect(range)"
      >
        <span class="range-number">{{ range.index }}</span>
        Between <strong>{{ range.low }}</strong> and <strong>{{ range.high }}</strong>
      </button>
    </div>
  </div>
</template>

<style scoped>
.range-list {
  display: flex;
  flex-direction: column;
}
</style>
