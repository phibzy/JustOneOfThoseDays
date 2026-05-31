"""
Pydantic models for the API request/response schemas.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, model_validator


class PlayerSpec(BaseModel):
    name: str = Field("", description="Player name (may be blank for a default)")
    is_cpu: bool = Field(False, description="Whether this slot is controlled by a CPU")


class CreateGameRequest(BaseModel):
    # Either provide a plain list of names (all human) ...
    player_names: Optional[List[str]] = Field(
        None, description="List of human player names"
    )
    # ... or a structured list of slots that may include CPUs.
    players: Optional[List[PlayerSpec]] = Field(
        None, description="List of player slots (human or CPU)"
    )

    def resolved_players(self) -> List[PlayerSpec]:
        """Return the effective list of player slots for this request."""
        if self.players:
            return self.players
        if self.player_names:
            return [PlayerSpec(name=name, is_cpu=False) for name in self.player_names]
        return []

    @model_validator(mode="after")
    def _validate_player_count(self) -> "CreateGameRequest":
        count = len(self.resolved_players())
        if count < 2 or count > 8:
            raise ValueError("A game must have between 2 and 8 players")
        return self


class JoinGameRequest(BaseModel):
    player_name: str = Field(..., min_length=1, description="Player name to join as")


class SubmitGuessRequest(BaseModel):
    guess_index: int = Field(
        ..., ge=0, description="0-based index of the chosen range"
    )


class RangeInfo(BaseModel):
    low: float
    high: float


class RangeOption(BaseModel):
    index: int
    low: float
    high: float


class CardInfo(BaseModel):
    desc: str
    value: Optional[float] = None


class PlayerInfo(BaseModel):
    name: str
    num_cards: int
    is_cpu: bool = False
    hand: Optional[Dict[str, Any]] = None


class GameStateResponse(BaseModel):
    game_id: str
    state: str
    current_card: Optional[CardInfo] = None
    current_card_value: Optional[float] = None
    current_guesser: str
    current_guesser_index: int
    current_starter: str
    players: List[PlayerInfo]
    previous_guesses: List[RangeInfo]
    deck_remaining: int
    messages: List[str]
    winner: Optional[str] = None
    guesser_ranges: List[RangeOption]
    guesser_hand: List[CardInfo]
    # Per-player extras
    my_hand: Optional[Dict[str, Any]] = None
    is_my_turn: Optional[bool] = None


class GameCreatedResponse(BaseModel):
    game_id: str
    join_url: str
    player_tokens: Dict[str, str]


class JoinedGameResponse(BaseModel):
    player_name: str
    player_token: str
    game_id: str


class ErrorResponse(BaseModel):
    error: str
