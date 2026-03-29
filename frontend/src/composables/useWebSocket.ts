/** WebSocket composable for real-time game communication. */

import { ref, onUnmounted } from 'vue'
import type { GameState } from '../types/game'

export function useWebSocket() {
  const gameState = ref<GameState | null>(null)
  const isConnected = ref(false)
  const error = ref<string | null>(null)
  let ws: WebSocket | null = null

  function connect(gameId: string, token: string) {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = window.location.host
    const url = `${protocol}//${host}/ws/game/${gameId}?token=${encodeURIComponent(token)}`

    ws = new WebSocket(url)

    ws.onopen = () => {
      isConnected.value = true
      error.value = null
    }

    ws.onmessage = (event: MessageEvent) => {
      try {
        const data = JSON.parse(event.data)
        if (data.error) {
          error.value = data.error
        } else {
          gameState.value = data as GameState
        }
      } catch {
        error.value = 'Failed to parse server message'
      }
    }

    ws.onclose = () => {
      isConnected.value = false
    }

    ws.onerror = () => {
      error.value = 'WebSocket connection error'
      isConnected.value = false
    }
  }

  function sendGuess(guessIndex: number) {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'guess', guess_index: guessIndex }))
    }
  }

  function disconnect() {
    if (ws) {
      ws.close()
      ws = null
    }
  }

  onUnmounted(() => {
    disconnect()
  })

  return {
    gameState,
    isConnected,
    error,
    connect,
    sendGuess,
    disconnect,
  }
}
