/** Game-related TypeScript types. */

export interface CardInfo {
  desc: string
  value?: number
}

export interface RangeOption {
  index: number
  low: number
  high: number
}

export interface RangeInfo {
  low: number
  high: number
}

export interface HandInfo {
  cards: CardInfo[]
  ranges: RangeOption[]
  num_cards: number
  num_ranges: number
}

export interface PlayerInfo {
  name: string
  num_cards: number
  is_cpu?: boolean
  hand?: HandInfo
}

export interface PlayerSlot {
  name: string
  is_cpu: boolean
}

export interface GameState {
  game_id: string
  state: 'waiting_for_players' | 'waiting_for_guess' | 'game_over'
  current_card: CardInfo | null
  current_card_value: number | null
  current_guesser: string
  current_guesser_index: number
  current_starter: string
  players: PlayerInfo[]
  previous_guesses: RangeInfo[]
  deck_remaining: number
  messages: string[]
  winner: string | null
  guesser_ranges: RangeOption[]
  guesser_hand: CardInfo[]
  // Per-player extras
  my_hand?: HandInfo
  is_my_turn?: boolean
}

export interface GameCreatedResponse {
  game_id: string
  join_url: string
  player_tokens: Record<string, string>
}

export interface WebSocketMessage {
  type: 'guess'
  guess_index: number
}
