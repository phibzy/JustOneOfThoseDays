<script setup lang="ts">
import type { PlayerInfo } from '../types/game'

defineProps<{
  players: PlayerInfo[]
  currentGuesser: string
  myName: string
}>()
</script>

<template>
  <div class="panel">
    <div class="panel-header">
      <h3>Scoreboard</h3>
    </div>
    <div class="scoreboard">
      <div
        v-for="player in players"
        :key="player.name"
        class="scoreboard-item"
        :class="{
          active: player.name === currentGuesser,
          'is-me': player.name === myName,
        }"
      >
        <div class="player-name">
          {{ player.name }}
          <span v-if="player.name === myName" class="badge badge-info">You</span>
          <span v-else-if="player.is_cpu" class="badge badge-info">CPU</span>
        </div>
        <div class="player-cards">{{ player.num_cards }}</div>
        <div class="player-label">cards</div>
      </div>
    </div>
  </div>
</template>
