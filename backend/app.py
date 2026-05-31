"""
FastAPI application with REST and WebSocket endpoints for the game.
"""

import uuid
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware

from backend.models import (
    CreateGameRequest,
    ErrorResponse,
    GameCreatedResponse,
    GameStateResponse,
    SubmitGuessRequest,
)
from backend.game_manager import game_manager, GameSession
from backend.game.board import GameState

app = FastAPI(title="Just One Of Those Days", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
class ConnectionManager:
    """Manages WebSocket connections grouped by game_id."""

    def __init__(self) -> None:
        # game_id -> list of (websocket, player_name)
        self.active_connections: Dict[str, List[tuple[WebSocket, str]]] = {}

    async def connect(
        self, websocket: WebSocket, game_id: str, player_name: str
    ) -> None:
        await websocket.accept()
        if game_id not in self.active_connections:
            self.active_connections[game_id] = []
        self.active_connections[game_id].append((websocket, player_name))

    def disconnect(self, websocket: WebSocket, game_id: str) -> None:
        if game_id in self.active_connections:
            self.active_connections[game_id] = [
                (ws, name)
                for ws, name in self.active_connections[game_id]
                if ws != websocket
            ]
            if not self.active_connections[game_id]:
                del self.active_connections[game_id]

    async def broadcast_game_state(self, game_id: str, session: GameSession) -> None:
        """Send personalised game state to each connected player."""
        if game_id not in self.active_connections:
            return
        for websocket, player_name in self.active_connections[game_id]:
            try:
                state = session.get_state(player_name)
                state["game_id"] = game_id
                await websocket.send_json(state)
            except Exception:
                pass


ws_manager = ConnectionManager()


# --- REST Endpoints ---


@app.post("/api/game", response_model=GameCreatedResponse)
async def create_game(request: CreateGameRequest) -> GameCreatedResponse:
    """Create a new game with the given player slots (humans and/or CPUs)."""
    specs = request.resolved_players()
    player_names = [spec.name for spec in specs]
    cpu_flags = [spec.is_cpu for spec in specs]

    game_id = str(uuid.uuid4())[:8]
    session = game_manager.create_game(game_id, player_names, cpu_flags)

    # Start the game immediately, then auto-play any leading CPU turns.
    session.start()
    session.advance_cpu_turns()
    game_manager.save()

    return GameCreatedResponse(
        game_id=game_id,
        join_url=f"/game/{game_id}",
        player_tokens=session.player_tokens,
    )


@app.get("/api/game/{game_id}")
async def get_game_state(game_id: str, token: str = Query(...)) -> dict:
    """Get the current game state for a player."""
    session = game_manager.get_game(game_id)
    if not session:
        raise HTTPException(status_code=404, detail="Game not found")

    player_name = session.get_player_by_token(token)
    if not player_name:
        raise HTTPException(status_code=403, detail="Invalid token")

    state = session.get_state(player_name)
    state["game_id"] = game_id
    return state


@app.post("/api/game/{game_id}/guess")
async def submit_guess(
    game_id: str, request: SubmitGuessRequest, token: str = Query(...)
) -> dict:
    """Submit a range guess for the current card."""
    session = game_manager.get_game(game_id)
    if not session:
        raise HTTPException(status_code=404, detail="Game not found")

    player_name = session.get_player_by_token(token)
    if not player_name:
        raise HTTPException(status_code=403, detail="Invalid token")

    # Verify it's this player's turn
    current_guesser = session.board.players[session.board.current_guesser]
    if current_guesser.name != player_name:
        raise HTTPException(status_code=400, detail="Not your turn")

    state = session.submit_guess(request.guess_index)
    # Auto-play any CPU turns that follow this guess.
    session.advance_cpu_turns()
    game_manager.save()
    state = session.get_state(player_name)
    state["game_id"] = game_id

    # Broadcast updated state to all connected players
    await ws_manager.broadcast_game_state(game_id, session)

    return state


# --- WebSocket Endpoint ---


@app.websocket("/ws/game/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str) -> None:
    """WebSocket connection for real-time game updates."""
    token = websocket.query_params.get("token", "")
    session = game_manager.get_game(game_id)

    if not session:
        await websocket.close(code=4004, reason="Game not found")
        return

    player_name = session.get_player_by_token(token)
    if not player_name:
        await websocket.close(code=4003, reason="Invalid token")
        return

    await ws_manager.connect(websocket, game_id, player_name)
    session.connected_players.add(player_name)

    try:
        # Send initial state
        state = session.get_state(player_name)
        state["game_id"] = game_id
        await websocket.send_json(state)

        # Listen for messages (guess submissions via WebSocket)
        while True:
            data = await websocket.receive_json()

            if data.get("type") == "guess":
                # Verify it's this player's turn
                current_guesser = session.board.players[
                    session.board.current_guesser
                ]
                if current_guesser.name != player_name:
                    await websocket.send_json(
                        {"error": "Not your turn"}
                    )
                    continue

                if session.board.state != GameState.WAITING_FOR_GUESS:
                    await websocket.send_json(
                        {"error": "Game is not waiting for a guess"}
                    )
                    continue

                guess_index = data.get("guess_index", -1)
                session.submit_guess(guess_index)
                # Auto-play any CPU turns that follow this guess.
                session.advance_cpu_turns()
                game_manager.save()

                # Broadcast to all players
                await ws_manager.broadcast_game_state(game_id, session)

    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, game_id)
        session.connected_players.discard(player_name)
