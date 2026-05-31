<script setup lang="ts">
import { computed } from 'vue'
import { useGameStore } from '../stores/game'
import CardDisplay from './CardDisplay.vue'
import PlayerHand from './PlayerHand.vue'
import RangeSelector from './RangeSelector.vue'
import Scoreboard from './Scoreboard.vue'
import Timer from './Timer.vue'
import MessageLog from './MessageLog.vue'
import GameOver from './GameOver.vue'

const store = useGameStore()

const emit = defineEmits<{
  (e: 'guess', index: number): void
  (e: 'play-again'): void
}>()

const myHandCards = computed(() => {
  return store.myHand?.cards ?? []
})

const myRanges = computed(() => {
  return store.myHand?.ranges ?? []
})

function handleGuess(index: number) {
  emit('guess', index)
}
</script>

<template>
  <div class="game-layout" v-if="store.gameState">
    <!-- Left sidebar: Your hand -->
    <div class="game-sidebar-left">
      <PlayerHand :cards="myHandCards" title="Your Hand" />
      <MessageLog :messages="store.messages" />
    </div>

    <!-- Main area: Card + Range selector -->
    <div class="game-main">
      <!-- Header -->
      <div class="game-header">
        <span class="game-title">Just One Of Those Days</span>
        <div class="deck-indicator">
          🃏 <span class="deck-count">{{ store.deckRemaining }}</span> cards left
        </div>
      </div>

      <!-- Turn indicator -->
      <div
        class="turn-indicator"
        :class="store.isMyTurn ? 'my-turn' : 'other-turn'"
      >
        <template v-if="store.isMyTurn">
          🎯 It's your turn! Choose a range below.
        </template>
        <template v-else>
          ⏳ Waiting for <strong>{{ store.currentGuesser }}</strong> to guess...
        </template>
        <Timer
          v-if="store.isMyTurn && !store.isGameOver"
          :active="store.isMyTurn"
          :duration="30"
          @timeout="handleGuess(0)"
          style="margin-left: 12px;"
        />
      </div>

      <!-- Current card -->
      <CardDisplay
        v-if="store.currentCard"
        :card="store.currentCard"
        :show-value="store.isGameOver"
        size="large"
      />

      <!-- Range selector (only shown on your turn) -->
      <RangeSelector
        v-if="store.isMyTurn && !store.isGameOver"
        :ranges="myRanges"
        :previous-guesses="store.previousGuesses"
        :disabled="!store.isMyTurn || store.loading"
        @select="handleGuess"
      />

      <!-- Previous wrong guesses info -->
      <div
        v-if="store.previousGuesses.length > 0 && !store.isGameOver"
        class="panel"
        style="text-align: center;"
      >
        <p style="color: var(--text-muted); margin-bottom: 8px;">
          Previously guessed (wrong):
        </p>
        <div style="display: flex; gap: 8px; justify-content: center; flex-wrap: wrap;">
          <span
            v-for="(g, i) in store.previousGuesses"
            :key="i"
            class="badge badge-accent"
          >
            {{ g.low }} – {{ g.high }}
          </span>
        </div>
      </div>
    </div>

    <!-- Right sidebar: Scoreboard -->
    <div class="game-sidebar-right">
      <Scoreboard
        :players="store.players"
        :current-guesser="store.currentGuesser"
        :my-name="store.playerName || ''"
      />
    </div>

    <!-- Game over overlay -->
    <GameOver
      v-if="store.isGameOver"
      :winner="store.winner"
      :players="store.players"
      @play-again="emit('play-again')"
    />
  </div>
</template>
