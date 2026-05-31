"""
Game manager with on-disk persistence.

Stores active games and manages player tokens/sessions. Game state is
persisted to a JSON file so that in-progress games survive a server restart.
"""

import json
import os
import secrets
import tempfile
from typing import Any, Dict, List, Optional, Set

from backend.game.board import Board, GameState


class GameSession:
    """Wraps a Board with session management (player tokens, connections)."""

    def __init__(
        self,
        game_id: str,
        player_names: List[str],
        cpu_flags: Optional[List[bool]] = None,
    ) -> None:
        self.game_id = game_id
        self.board = Board(player_names, cpu_flags)

        # Map player_name -> token for authentication
        self.player_tokens: Dict[str, str] = {}
        # Map token -> player_name for reverse lookup
        self.token_to_player: Dict[str, str] = {}
        # Track connected WebSocket player names
        self.connected_players: Set[str] = set()

        # Generate tokens for all human players (CPUs never connect)
        for player in self.board.players:
            if player.is_cpu:
                continue
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

    def advance_cpu_turns(self) -> Dict[str, Any]:
        """Auto-play any pending CPU turns."""
        return self.board.advance_cpu_turns()

    def get_state(self, player_name: Optional[str] = None) -> Dict[str, Any]:
        """Get game state, optionally tailored for a specific player."""
        if player_name:
            return self.board.get_player_state(player_name)
        return self.board.get_game_state()

    def serialize(self) -> Dict[str, Any]:
        """Return a fully persistable representation of the session."""
        return {
            "game_id": self.game_id,
            "board": self.board.serialize(),
            "player_tokens": self.player_tokens,
            "token_to_player": self.token_to_player,
        }

    @classmethod
    def from_serialized(cls, data: Dict[str, Any]) -> "GameSession":
        """Reconstruct a GameSession from its serialized representation."""
        session = cls.__new__(cls)
        session.game_id = data["game_id"]
        session.board = Board.from_serialized(data["board"])
        session.player_tokens = dict(data["player_tokens"])
        session.token_to_player = dict(data["token_to_player"])
        session.connected_players = set()
        return session


class GameManager:
    """Manages all active game sessions, persisting them to disk."""

    def __init__(self, storage_path: Optional[str] = None) -> None:
        self._games: Dict[str, GameSession] = {}
        self.storage_path: Optional[str] = (
            storage_path
            if storage_path is not None
            else os.environ.get("JUSTONE_STATE_FILE", "game_state.json")
        )
        self._load()

    def create_game(
        self,
        game_id: str,
        player_names: List[str],
        cpu_flags: Optional[List[bool]] = None,
    ) -> GameSession:
        """Create a new game session."""
        session = GameSession(game_id, player_names, cpu_flags)
        self._games[game_id] = session
        self.save()
        return session

    def get_game(self, game_id: str) -> Optional[GameSession]:
        """Retrieve a game session by ID."""
        return self._games.get(game_id)

    def remove_game(self, game_id: str) -> None:
        """Remove a completed game."""
        self._games.pop(game_id, None)
        self.save()

    def list_games(self) -> List[str]:
        """List all active game IDs."""
        return list(self._games.keys())

    # --- Persistence ---

    def save(self) -> None:
        """Persist all game sessions to disk atomically."""
        if not self.storage_path:
            return
        try:
            data = {gid: s.serialize() for gid, s in self._games.items()}
            directory = os.path.dirname(os.path.abspath(self.storage_path))
            os.makedirs(directory, exist_ok=True)
            fd, tmp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    json.dump(data, f)
                os.replace(tmp_path, self.storage_path)
            except Exception:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                raise
        except Exception:
            # Persistence must never crash gameplay.
            pass

    def _load(self) -> None:
        """Load persisted game sessions from disk, if any."""
        if not self.storage_path or not os.path.exists(self.storage_path):
            return
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for game_id, session_data in data.items():
                self._games[game_id] = GameSession.from_serialized(session_data)
        except Exception:
            # Ignore corrupt/incompatible state rather than failing startup.
            self._games = {}


# Singleton instance
game_manager = GameManager()
