<script setup lang="ts">
import type { PlayerInfo } from '../types/game'

defineProps<{
  winner: string | null
  players: PlayerInfo[]
}>()

const emit = defineEmits<{
  (e: 'play-again'): void
}>()
</script>

<template>
  <div class="game-over-overlay">
    <div class="game-over-panel panel">
      <div class="trophy">🏆</div>
      <div v-if="winner" class="winner-name">{{ winner }} Wins!</div>
      <div v-else class="winner-name">No Winner</div>
      <p class="winner-subtitle">
        {{ winner ? 'Congratulations!' : 'Nobody managed to win this time.' }}
      </p>

      <div style="margin-bottom: 24px;">
        <h3 style="margin-bottom: 12px;">Final Scores</h3>
        <div class="scoreboard">
          <div
            v-for="player in players"
            :key="player.name"
            class="scoreboard-item"
            :class="{ active: player.name === winner }"
          >
            <div class="player-name">{{ player.name }}</div>
            <div class="player-cards">{{ player.num_cards }}</div>
            <div class="player-label">cards</div>
          </div>
        </div>
      </div>

      <button class="btn btn-primary btn-lg" @click="emit('play-again')">
        Play Again
      </button>
    </div>
  </div>
</template>
