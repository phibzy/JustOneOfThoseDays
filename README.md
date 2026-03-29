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
2. Enter 2–8 player names in the lobby and click **Start Game**
3. Share the generated links with each player (each player opens their link in their own browser)
4. Each round, a card is drawn and its description is shown (but not its Misery Index value)
5. The current guesser chooses which range in their hand the card's value falls into
6. Correct guess → gain the card! Wrong guess → next player tries
7. First to 10 cards wins, or highest card count when the deck runs out

## Game Rules

- 2–8 Players
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


