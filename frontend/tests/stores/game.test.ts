import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useGameStore } from '../../src/stores/game'
import type { GameState } from '../../src/types/game'

describe('Game Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initializes with null values', () => {
    const store = useGameStore()
    expect(store.gameId).toBeNull()
    expect(store.playerName).toBeNull()
    expect(store.playerToken).toBeNull()
    expect(store.gameState).toBeNull()
    expect(store.loading).toBe(false)
    expect(store.error).toBeNull()
  })

  it('sets player correctly', () => {
    const store = useGameStore()
    store.setPlayer('Alice', 'token123')
    expect(store.playerName).toBe('Alice')
    expect(store.playerToken).toBe('token123')
  })

  it('joins existing game correctly', () => {
    const store = useGameStore()
    store.joinExistingGame('game1', 'Alice', 'token123')
    expect(store.gameId).toBe('game1')
    expect(store.playerName).toBe('Alice')
    expect(store.playerToken).toBe('token123')
  })

  it('resets game state', () => {
    const store = useGameStore()
    store.joinExistingGame('game1', 'Alice', 'token123')
    store.resetGame()
    expect(store.gameId).toBeNull()
    expect(store.playerName).toBeNull()
    expect(store.playerToken).toBeNull()
    expect(store.gameState).toBeNull()
  })

  it('computes isMyTurn correctly', () => {
    const store = useGameStore()
    store.setPlayer('Alice', 'token123')

    const mockState: GameState = {
      game_id: 'test',
      state: 'waiting_for_guess',
      current_card: { desc: 'Test card' },
      current_card_value: null,
      current_guesser: 'Alice',
      current_guesser_index: 0,
      current_starter: 'Alice',
      players: [
        { name: 'Alice', num_cards: 3 },
        { name: 'Bob', num_cards: 3 },
      ],
      previous_guesses: [],
      deck_remaining: 90,
      messages: [],
      winner: null,
      guesser_ranges: [{ index: 1, low: 0, high: 100 }],
      guesser_hand: [{ desc: 'Card 1', value: 50 }],
      is_my_turn: true,
    }
    store.setGameState(mockState)
    expect(store.isMyTurn).toBe(true)
  })

  it('computes isMyTurn as false when not my turn', () => {
    const store = useGameStore()
    store.setPlayer('Alice', 'token123')

    const mockState: GameState = {
      game_id: 'test',
      state: 'waiting_for_guess',
      current_card: { desc: 'Test card' },
      current_card_value: null,
      current_guesser: 'Bob',
      current_guesser_index: 1,
      current_starter: 'Alice',
      players: [
        { name: 'Alice', num_cards: 3 },
        { name: 'Bob', num_cards: 3 },
      ],
      previous_guesses: [],
      deck_remaining: 90,
      messages: [],
      winner: null,
      guesser_ranges: [],
      guesser_hand: [],
      is_my_turn: false,
    }
    store.setGameState(mockState)
    expect(store.isMyTurn).toBe(false)
  })

  it('computes isGameOver correctly', () => {
    const store = useGameStore()
    const mockState: GameState = {
      game_id: 'test',
      state: 'game_over',
      current_card: null,
      current_card_value: null,
      current_guesser: 'Alice',
      current_guesser_index: 0,
      current_starter: 'Alice',
      players: [
        { name: 'Alice', num_cards: 10 },
        { name: 'Bob', num_cards: 3 },
      ],
      previous_guesses: [],
      deck_remaining: 0,
      messages: ['Alice wins!'],
      winner: 'Alice',
      guesser_ranges: [],
      guesser_hand: [],
    }
    store.setGameState(mockState)
    expect(store.isGameOver).toBe(true)
    expect(store.winner).toBe('Alice')
  })

  it('computes players list', () => {
    const store = useGameStore()
    const mockState: GameState = {
      game_id: 'test',
      state: 'waiting_for_guess',
      current_card: { desc: 'Test' },
      current_card_value: null,
      current_guesser: 'Alice',
      current_guesser_index: 0,
      current_starter: 'Alice',
      players: [
        { name: 'Alice', num_cards: 3 },
        { name: 'Bob', num_cards: 4 },
        { name: 'Charlie', num_cards: 5 },
      ],
      previous_guesses: [],
      deck_remaining: 80,
      messages: [],
      winner: null,
      guesser_ranges: [],
      guesser_hand: [],
    }
    store.setGameState(mockState)
    expect(store.players).toHaveLength(3)
    expect(store.players[0].name).toBe('Alice')
  })

  it('computes messages', () => {
    const store = useGameStore()
    const mockState: GameState = {
      game_id: 'test',
      state: 'waiting_for_guess',
      current_card: { desc: 'Test' },
      current_card_value: null,
      current_guesser: 'Alice',
      current_guesser_index: 0,
      current_starter: 'Alice',
      players: [],
      previous_guesses: [],
      deck_remaining: 80,
      messages: ['Hello', 'World'],
      winner: null,
      guesser_ranges: [],
      guesser_hand: [],
    }
    store.setGameState(mockState)
    expect(store.messages).toEqual(['Hello', 'World'])
  })

  it('computes previousGuesses', () => {
    const store = useGameStore()
    const mockState: GameState = {
      game_id: 'test',
      state: 'waiting_for_guess',
      current_card: { desc: 'Test' },
      current_card_value: null,
      current_guesser: 'Bob',
      current_guesser_index: 1,
      current_starter: 'Alice',
      players: [],
      previous_guesses: [{ low: 0, high: 50 }],
      deck_remaining: 80,
      messages: [],
      winner: null,
      guesser_ranges: [],
      guesser_hand: [],
    }
    store.setGameState(mockState)
    expect(store.previousGuesses).toHaveLength(1)
    expect(store.previousGuesses[0]).toEqual({ low: 0, high: 50 })
  })

  it('computes deckRemaining', () => {
    const store = useGameStore()
    const mockState: GameState = {
      game_id: 'test',
      state: 'waiting_for_guess',
      current_card: { desc: 'Test' },
      current_card_value: null,
      current_guesser: 'Alice',
      current_guesser_index: 0,
      current_starter: 'Alice',
      players: [],
      previous_guesses: [],
      deck_remaining: 42,
      messages: [],
      winner: null,
      guesser_ranges: [],
      guesser_hand: [],
    }
    store.setGameState(mockState)
    expect(store.deckRemaining).toBe(42)
  })
})
