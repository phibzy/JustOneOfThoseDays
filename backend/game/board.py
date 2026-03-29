"""
Represents the board of the game.
Keeps track of the current game state.

Refactored to be a state machine that can be driven externally
(by an API/WebSocket layer) rather than a synchronous game loop.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import random

from backend.game.player import Player
from backend.game.card import Card
from backend.game.card_list import card_list
from backend.game.exceptions import NoCardError, NumPlayerError


class GameState(str, Enum):
    WAITING_FOR_PLAYERS = "waiting_for_players"
    WAITING_FOR_GUESS = "waiting_for_guess"
    GAME_OVER = "game_over"


class Board:
    """
    Main game controller — manages game state and turn flow.

    Converted from a synchronous game loop to a state machine that
    can be driven by external callers (API endpoints).
    """

    STARTING_CARDS = 3
    MAX_PLAYERS = 8
    WIN_CARD_COUNT = 10

    def __init__(self, player_names: List[str]) -> None:
        # Create the game deck + discard pile
        self.discard_pile: List[Card] = []
        self.deck: List[Card] = self._initialise_deck()
        random.shuffle(self.deck)
        self.num_cards: int = len(self.deck)

        # Players
        self.players: List[Player] = []
        self.current_guesser: int = 0
        self.current_starter: int = 0
        self.current_leader: Optional[Player] = None
        self.num_players: int = 0

        # Game state
        self.state: GameState = GameState.WAITING_FOR_PLAYERS
        self.current_card: Optional[Card] = None
        self.previous_guesses: List[Tuple[float, float]] = []
        self.message_log: List[str] = []
        self.winner: Optional[Player] = None

        # Initialise players (validates count, handles duplicates, deals cards)
        self._initialise_players(player_names)

    def start_game(self) -> Dict[str, Any]:
        """Start the game by drawing the first card. Returns game state."""
        self.current_card = self._draw_card()
        self.state = GameState.WAITING_FOR_GUESS
        self.message_log = []
        self._add_message(
            f"{self.players[self.current_starter].name} starts the round!"
        )
        return self.get_game_state()

    def submit_guess(self, guess_index: int) -> Dict[str, Any]:
        """
        Process a player's guess. Returns updated game state.

        Args:
            guess_index: 0-based index into the current guesser's ranges.
        """
        if self.state != GameState.WAITING_FOR_GUESS:
            return self.get_game_state()

        player = self.players[self.current_guesser]
        self.message_log = []

        # Validate guess index
        if guess_index < 0 or guess_index >= player.num_ranges:
            self._add_message(
                f"{player.name} made an invalid guess — counts as wrong!"
            )
            return self._handle_wrong_guess()

        # Check if the guess is correct
        guessed_range = player.guessed_range(guess_index)
        if guessed_range[0] <= self.current_card.value <= guessed_range[1]:
            return self._handle_correct_guess(player)
        else:
            self._add_message(f"{player.name}'s guess was incorrect!")
            self.previous_guesses.append(guessed_range)
            return self._handle_wrong_guess()

    def get_game_state(self) -> Dict[str, Any]:
        """Return the full game state as a dictionary for serialization."""
        current_guesser_player = self.players[self.current_guesser]
        return {
            "state": self.state.value,
            "current_card": (
                self.current_card.to_dict(hide_value=True)
                if self.current_card
                else None
            ),
            "current_card_value": (
                self.current_card.value
                if self.current_card and self.state == GameState.GAME_OVER
                else None
            ),
            "current_guesser": current_guesser_player.name,
            "current_guesser_index": self.current_guesser,
            "current_starter": self.players[self.current_starter].name,
            "players": [p.to_dict(include_hand=True) for p in self.players],
            "previous_guesses": [
                {"low": g[0], "high": g[1]} for g in self.previous_guesses
            ],
            "deck_remaining": self.num_cards,
            "messages": list(self.message_log),
            "winner": self.winner.name if self.winner else None,
            "guesser_ranges": current_guesser_player.hand.get_ranges_list(),
            "guesser_hand": current_guesser_player.hand.get_cards_list(),
        }

    def get_player_state(self, player_name: str) -> Optional[Dict[str, Any]]:
        """Return state tailored for a specific player (shows their full hand)."""
        base_state = self.get_game_state()
        # Find the requesting player and include their full hand details
        for p in self.players:
            if p.name == player_name:
                base_state["my_hand"] = p.hand.to_dict()
                base_state["is_my_turn"] = (
                    self.players[self.current_guesser].name == player_name
                )
                break
        return base_state

    # --- Private helper methods ---

    def _add_message(self, msg: str) -> None:
        self.message_log.append(msg)

    def _handle_correct_guess(self, player: Player) -> Dict[str, Any]:
        """Handle a correct guess: award card, check win, advance round."""
        player.gain_card(self.current_card)
        self._add_message(
            f"{player.name} guessed correctly! "
            f"The value was {self.current_card.value}. Card gained!"
        )

        # Update leader
        if (
            self.current_leader is None
            or player.num_cards > self.current_leader.num_cards
        ):
            self.current_leader = player

        # Check victory: player reached WIN_CARD_COUNT
        if player.num_cards >= self.WIN_CARD_COUNT:
            return self._end_game(player)

        # Check victory: deck empty
        if self.num_cards == 0:
            return self._end_game(None)

        # Start new round
        self._next_turn()
        self.current_card = self._draw_card()
        self._add_message(
            f"New round! {self.players[self.current_starter].name} starts."
        )
        return self.get_game_state()

    def _handle_wrong_guess(self) -> Dict[str, Any]:
        """Handle a wrong guess: advance to next guesser or end round."""
        if not self._next_guesser():
            # Everyone has guessed wrong
            self._add_message(
                f"Everyone failed! The correct value was "
                f"{self.current_card.value}."
            )
            self.discard_pile.append(self.current_card)

            # Check victory: deck empty
            if self.num_cards == 0:
                return self._end_game(None)

            # Start new round
            self._next_turn()
            self.current_card = self._draw_card()
            self._add_message(
                f"New round! {self.players[self.current_starter].name} starts."
            )
        else:
            next_player = self.players[self.current_guesser]
            self._add_message(f"Now it's {next_player.name}'s turn to guess.")

        return self.get_game_state()

    def _end_game(self, trigger_player: Optional[Player]) -> Dict[str, Any]:
        """End the game and determine the winner."""
        self.state = GameState.GAME_OVER

        if trigger_player and trigger_player.num_cards >= self.WIN_CARD_COUNT:
            self.winner = trigger_player
            self._add_message(
                f"{trigger_player.name} reached {self.WIN_CARD_COUNT} cards and wins!"
            )
        elif self.current_leader:
            self.winner = self.current_leader
            self._add_message(
                f"Deck is empty! {self.current_leader.name} wins with "
                f"{self.current_leader.num_cards} cards!"
            )
        else:
            self._add_message("Game over — no one wins!")

        return self.get_game_state()

    def _draw_card(self) -> Card:
        """Draw a card from the deck."""
        try:
            next_card = self.deck.pop()
            self.num_cards -= 1
        except IndexError:
            raise NoCardError("No more cards left in deck!")
        return next_card

    def _next_guesser(self) -> Optional[Player]:
        """Advance to the next guesser. Returns None when all have guessed."""
        self.current_guesser = (self.current_guesser + 1) % self.num_players
        if self.current_guesser == self.current_starter:
            return None
        return self.players[self.current_guesser]

    def _next_turn(self) -> None:
        """Advance to the next round."""
        self.current_starter = (self.current_starter + 1) % self.num_players
        self.current_guesser = self.current_starter
        self.previous_guesses = []

    # --- Initialisation ---

    def _initialise_deck(self) -> List[Card]:
        """Create list of cards from the card list."""
        return [Card(desc, index) for desc, index in card_list]

    def _initialise_players(self, player_names: List[str]) -> None:
        """Validate and create players, handling duplicate names."""
        # Create Player objects
        players = [Player(name) for name in player_names]

        names: Dict[str, int] = {}
        for player in players:
            next_name = player.name
            if not next_name:
                next_name = "Gary"

            if next_name in names:
                a = names[next_name]
                while (next_name + f"({a})") in names:
                    a += 1
                next_name += f"({a})"
                names[player.name] = a

            player.name = next_name
            self.players.append(player)
            names[next_name] = 1

        self.num_players = len(self.players)

        if self.num_players < 2:
            raise NumPlayerError("Error - Must have at least two players")
        if self.num_players > self.MAX_PLAYERS:
            raise NumPlayerError(
                f"Error - Can't have more than {self.MAX_PLAYERS} players."
            )

        # Deal starting cards
        self._initialise_player_cards()

        # Shuffle players for random starter
        random.shuffle(self.players)
        self.current_starter = 0
        self.current_guesser = 0

    def _initialise_player_cards(self) -> None:
        """Each player starts with STARTING_CARDS cards."""
        for player in self.players:
            for _ in range(self.STARTING_CARDS):
                player.gain_card(self._draw_card())
