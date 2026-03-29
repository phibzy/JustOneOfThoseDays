"""
Tests for the FastAPI endpoints.
"""

import pytest
from httpx import AsyncClient, ASGITransport

from backend.app import app
from backend.game_manager import game_manager


@pytest.fixture(autouse=True)
def clear_games():
    """Clear all games before each test."""
    game_manager._games.clear()
    yield
    game_manager._games.clear()


@pytest.mark.asyncio
async def test_create_game():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/game", json={"player_names": ["Alice", "Bob"]}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "game_id" in data
        assert "player_tokens" in data
        assert len(data["player_tokens"]) == 2


@pytest.mark.asyncio
async def test_create_game_too_few_players():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/game", json={"player_names": ["Alice"]})
        assert resp.status_code == 422


@pytest.mark.asyncio
async def test_get_game_state():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create game
        resp = await client.post(
            "/api/game", json={"player_names": ["Alice", "Bob"]}
        )
        data = resp.json()
        game_id = data["game_id"]
        tokens = data["player_tokens"]
        token = list(tokens.values())[0]

        # Get state
        resp = await client.get(f"/api/game/{game_id}?token={token}")
        assert resp.status_code == 200
        state = resp.json()
        assert state["state"] == "waiting_for_guess"
        assert "my_hand" in state
        assert "is_my_turn" in state


@pytest.mark.asyncio
async def test_get_game_state_invalid_token():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/game", json={"player_names": ["Alice", "Bob"]}
        )
        game_id = resp.json()["game_id"]

        resp = await client.get(f"/api/game/{game_id}?token=invalid")
        assert resp.status_code == 403


@pytest.mark.asyncio
async def test_get_nonexistent_game():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/game/fake?token=fake")
        assert resp.status_code == 404


@pytest.mark.asyncio
async def test_submit_guess():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create game
        resp = await client.post(
            "/api/game", json={"player_names": ["Alice", "Bob"]}
        )
        data = resp.json()
        game_id = data["game_id"]

        # Get current guesser state to find who goes first
        tokens = data["player_tokens"]

        # Get state to find current guesser
        first_token = list(tokens.values())[0]
        resp = await client.get(f"/api/game/{game_id}?token={first_token}")
        state = resp.json()
        current_guesser_name = state["current_guesser"]
        guesser_token = tokens[current_guesser_name]

        # Submit guess
        resp = await client.post(
            f"/api/game/{game_id}/guess?token={guesser_token}",
            json={"guess_index": 0},
        )
        assert resp.status_code == 200
        result = resp.json()
        assert "state" in result


@pytest.mark.asyncio
async def test_submit_guess_not_your_turn():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/game", json={"player_names": ["Alice", "Bob"]}
        )
        data = resp.json()
        game_id = data["game_id"]
        tokens = data["player_tokens"]

        # Find who is NOT the current guesser
        first_token = list(tokens.values())[0]
        resp = await client.get(f"/api/game/{game_id}?token={first_token}")
        state = resp.json()
        current_guesser_name = state["current_guesser"]

        # Find a different player's token
        non_guesser_token = None
        for name, token in tokens.items():
            if name != current_guesser_name:
                non_guesser_token = token
                break

        # Try to guess as wrong player
        resp = await client.post(
            f"/api/game/{game_id}/guess?token={non_guesser_token}",
            json={"guess_index": 0},
        )
        assert resp.status_code == 400
