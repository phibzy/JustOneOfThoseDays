<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useGameStore } from '../stores/game'
import { useWebSocket } from '../composables/useWebSocket'
import GameBoard from '../components/GameBoard.vue'

const route = useRoute()
const router = useRouter()
const store = useGameStore()
const { gameState, isConnected, connect, sendGuess: _sendGuess, disconnect } = useWebSocket()

const gameId = route.params.gameId as string
const playerName = (route.query.player as string) || ''
const token = (route.query.token as string) || ''

onMounted(() => {
  if (!playerName || !token) {
    router.push('/')
    return
  }

  store.joinExistingGame(gameId, playerName, token)
  connect(gameId, token)
})

// Watch for WebSocket state updates
import { watch } from 'vue'

watch(gameState, (newState) => {
  if (newState) {
    store.setGameState(newState)
  }
})

function handleGuess(index: number) {
  // Use HTTP for the guess to get a reliable response,
  // then let WebSocket broadcast the state update.
  store.submitGuess(index)
}

function handlePlayAgain() {
  disconnect()
  store.resetGame()
  router.push('/')
}

onUnmounted(() => {
  disconnect()
})
</script>

<template>
  <div v-if="!isConnected && !store.gameState" class="lobby-container">
    <div class="panel" style="text-align: center;">
      <p style="color: var(--text-muted);">Connecting to game...</p>
    </div>
  </div>
  <GameBoard
    v-else
    @guess="handleGuess"
    @play-again="handlePlayAgain"
  />
</template>
