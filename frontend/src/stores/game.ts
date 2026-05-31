/** Pinia store for game state management. */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { GameState, GameCreatedResponse, PlayerSlot } from '../types/game'

export const useGameStore = defineStore('game', () => {
  // State
  const gameId = ref<string | null>(null)
  const playerName = ref<string | null>(null)
  const playerToken = ref<string | null>(null)
  const gameState = ref<GameState | null>(null)
  const allTokens = ref<Record<string, string>>({})
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const isMyTurn = computed(() => {
    if (!gameState.value || !playerName.value) return false
    return gameState.value.current_guesser === playerName.value
  })

  const isGameOver = computed(() => {
    return gameState.value?.state === 'game_over'
  })

  const myHand = computed(() => {
    return gameState.value?.my_hand ?? null
  })

  const currentCard = computed(() => {
    return gameState.value?.current_card ?? null
  })

  const players = computed(() => {
    return gameState.value?.players ?? []
  })

  const winner = computed(() => {
    return gameState.value?.winner ?? null
  })

  const messages = computed(() => {
    return gameState.value?.messages ?? []
  })

  const previousGuesses = computed(() => {
    return gameState.value?.previous_guesses ?? []
  })

  const guesserRanges = computed(() => {
    return gameState.value?.guesser_ranges ?? []
  })

  const deckRemaining = computed(() => {
    return gameState.value?.deck_remaining ?? 0
  })

  const currentGuesser = computed(() => {
    return gameState.value?.current_guesser ?? ''
  })

  // Actions
  async function createGame(players: PlayerSlot[]): Promise<GameCreatedResponse> {
    loading.value = true
    error.value = null
    try {
      const resp = await fetch('/api/game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ players }),
      })
      if (!resp.ok) {
        const errData = await resp.json()
        throw new Error(errData.detail || 'Failed to create game')
      }
      const data: GameCreatedResponse = await resp.json()
      gameId.value = data.game_id
      allTokens.value = data.player_tokens
      return data
    } catch (e) {
      error.value = (e as Error).message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function fetchGameState(): Promise<void> {
    if (!gameId.value || !playerToken.value) return
    loading.value = true
    try {
      const resp = await fetch(
        `/api/game/${gameId.value}?token=${encodeURIComponent(playerToken.value)}`
      )
      if (!resp.ok) throw new Error('Failed to fetch game state')
      gameState.value = await resp.json()
    } catch (e) {
      error.value = (e as Error).message
    } finally {
      loading.value = false
    }
  }

  async function submitGuess(guessIndex: number): Promise<void> {
    if (!gameId.value || !playerToken.value) return
    loading.value = true
    error.value = null
    try {
      const resp = await fetch(
        `/api/game/${gameId.value}/guess?token=${encodeURIComponent(playerToken.value)}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ guess_index: guessIndex }),
        }
      )
      if (!resp.ok) {
        const errData = await resp.json()
        throw new Error(errData.detail || 'Failed to submit guess')
      }
      gameState.value = await resp.json()
    } catch (e) {
      error.value = (e as Error).message
    } finally {
      loading.value = false
    }
  }

  function setPlayer(name: string, token: string) {
    playerName.value = name
    playerToken.value = token
  }

  function setGameState(state: GameState) {
    gameState.value = state
  }

  function joinExistingGame(id: string, name: string, token: string) {
    gameId.value = id
    playerName.value = name
    playerToken.value = token
  }

  function resetGame() {
    gameId.value = null
    playerName.value = null
    playerToken.value = null
    gameState.value = null
    allTokens.value = {}
    loading.value = false
    error.value = null
  }

  return {
    // State
    gameId,
    playerName,
    playerToken,
    gameState,
    allTokens,
    loading,
    error,
    // Getters
    isMyTurn,
    isGameOver,
    myHand,
    currentCard,
    players,
    winner,
    messages,
    previousGuesses,
    guesserRanges,
    deckRemaining,
    currentGuesser,
    // Actions
    createGame,
    fetchGameState,
    submitGuess,
    setPlayer,
    setGameState,
    joinExistingGame,
    resetGame,
  }
})
