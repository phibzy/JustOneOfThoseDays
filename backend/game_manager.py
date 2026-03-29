"""
In-memory game manager.
Stores active games and manages player tokens/sessions.
"""

import secrets
from typing import Any, Dict, List, Optional, Set

from backend.game.board import Board, GameState


class GameSession:
    """Wraps a Board with session management (player tokens, connections)."""

    def __init__(self, game_id: str, player_names: List[str]) -> None:
        self.game_id = game_id
        self.board = Board(player_names)

        # Map player_name -> token for authentication
        self.player_tokens: Dict[str, str] = {}
        # Map token -> player_name for reverse lookup
        self.token_to_player: Dict[str, str] = {}
        # Track connected WebSocket player names
        self.connected_players: Set[str] = set()

        # Generate tokens for all players
        for player in self.board.players:
            token = secrets.token_urlsafe(32)
            self.player_tokens[player.name] = token
            self.token_to_player[token] = player.name

    def get_player_by_token(self, token: str) -> Optional[str]:
        """Look up player name by token."""
        return self.token_to_player.get(token)

    def start(self) -> Dict[str, Any]:
        """Start the game."""
        return self.board.start_game()

    def submit_guess(self, guess_index: int) -> Dict[str, Any]:
        """Submit a guess for the current guesser."""
        return self.board.submit_guess(guess_index)

    def get_state(self, player_name: Optional[str] = None) -> Dict[str, Any]:
        """Get game state, optionally tailored for a specific player."""
        if player_name:
            return self.board.get_player_state(player_name)
        return self.board.get_game_state()


class GameManager:
    """Manages all active game sessions in memory."""

    def __init__(self) -> None:
        self._games: Dict[str, GameSession] = {}

    def create_game(self, game_id: str, player_names: List[str]) -> GameSession:
        """Create a new game session."""
        session = GameSession(game_id, player_names)
        self._games[game_id] = session
        return session

    def get_game(self, game_id: str) -> Optional[GameSession]:
        """Retrieve a game session by ID."""
        return self._games.get(game_id)

    def remove_game(self, game_id: str) -> None:
        """Remove a completed game."""
        self._games.pop(game_id, None)

    def list_games(self) -> List[str]:
        """List all active game IDs."""
        return list(self._games.keys())


# Singleton instance
game_manager = GameManager()
