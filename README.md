# Just One Of Those Days
A Python implementation of Stuff/S*** Happens by Goliath Games. I am in no way affiliated with them, this is purely a hobby project.

## Architecture

The game consists of two parts:
- **Backend**: Python FastAPI server with WebSocket support for real-time multiplayer
- **Frontend**: Vue 3 + TypeScript single-page application built with Vite

Each player connects from their own browser. Game state is synchronized in real-time via WebSocket.

## Prerequisites
- Python 3.10+
- Node.js 18+

## Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn backend.app:app --reload
```

The API server runs on `http://localhost:8000`.

### Frontend
```bash
cd frontend
npm install
npm run dev
```

The dev server runs on `http://localhost:5173` and proxies API/WebSocket requests to the backend.

### Running Tests

**Backend tests (pytest):**
```bash
python -m pytest backend/tests/ -v
```

**Frontend tests (Vitest):**
```bash
cd frontend
npm run test
```

## How to Play

1. Open the app in your browser
2. In the lobby, add 2–8 slots and choose for each whether it is a **Human** or a **CPU** (use **+ Add Player** / **+ Add CPU**). At least one human is required.
3. Click **Start Game**
4. Share the generated links with each human player (each player opens their link in their own browser). CPU players take their turns automatically.
5. Each round, a card is drawn and its description is shown (but not its Misery Index value)
6. The current guesser chooses which range in their hand the card's value falls into
7. Correct guess → gain the card! Wrong guess → next player tries
8. First to 10 cards wins, or highest card count when the deck runs out

> **Note:** In-progress games are persisted to disk, so they survive a server
> restart. The state file location can be configured with the
> `JUSTONE_STATE_FILE` environment variable (defaults to `game_state.json`).

## Game Rules

- 2–8 Players (any slot may be filled by a human or a CPU; at least one human is required)
- Each player starts with 3 cards drawn from the deck
- Each card describes an unpleasant experience followed by its Misery Index: a number measuring how bad it is (100 being the most horrible experience possible)
- Each player's cards are ordered according to their Misery Index
- At the start of each round a new card is drawn and its description is revealed, but not its Misery Index
- Players take turns trying to guess where the card's Misery Index lies in relation to the value of their own cards
- If a player guesses correctly, the new card is added to their hand and a new round begins
- If a player guesses incorrectly, the next player has a turn at guessing
- If no one is able to guess correctly, the card is discarded and a new round begins
- Players take turns starting the round as the initial guesser

### Win Conditions
- A player reaches 10 cards
- The deck runs out of cards — the winner is the first player who reached the current high score


