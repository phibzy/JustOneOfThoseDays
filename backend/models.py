"""
Pydantic models for the API request/response schemas.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class CreateGameRequest(BaseModel):
    player_names: List[str] = Field(
        ..., min_length=2, max_length=8, description="List of player names"
    )


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
