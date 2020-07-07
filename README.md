# Just One Of Those Days
A Python implementation of Stuff/S*** Happens by Goliath Games. I am in no way affiliated with them, this is purely a hobby project. Written for Python 3.6.9+ on Unix systems. Current version is entirely text-based.

# Starting Rules
- 2+ Players
- Each player starts with 3 cards drawn from the deck

Each card describes an unpleasant experience followed by its Misery Index: a number measuring how bad it is (100 being the most horrible experience possible). Each player's cards are ordered according to their Misery Index.

# Round

- At the start of the round a new card is drawn from the deck and its description is revealed, but not its misery index
- Players take turns trying to guess where the card's misery index lies in relation to the value of their own cards (e.g. between 35 and 42)
- If a player guesses correctly, the new card is added to their hand and a new round begins
- If a player guesses incorrectly, the next player has a turn at guessing
- If no one is able to guess it correctly the card is discarded and a new round begins
- Players take turns starting the round as the initial guesser

# Win Conditions

- A player reaches 10 cards
- The deck runs out of cards, the winner is the first player who reached the current high score


