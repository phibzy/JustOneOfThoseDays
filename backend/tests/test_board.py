"""
Tests for the refactored Board class (state machine).
"""

import random
import unittest

from backend.game.board import Board, GameState
from backend.game.card import Card
from backend.game.exceptions import NumPlayerError


class TestBoardInit(unittest.TestCase):
    def test_basic_creation(self):
        random.seed(42)
        board = Board(["Alice", "Bob"])
        self.assertEqual(board.num_players, 2)
        self.assertEqual(board.state, GameState.WAITING_FOR_PLAYERS)
        # Each player should have 3 starting cards
        for p in board.players:
            self.assertEqual(p.num_cards, 3)

    def test_too_few_players(self):
        with self.assertRaises(NumPlayerError):
            Board(["Alice"])

    def test_too_many_players(self):
        with self.assertRaises(NumPlayerError):
            Board([f"Player{i}" for i in range(9)])

    def test_duplicate_names(self):
        random.seed(42)
        board = Board(["Bob", "Bob"])
        names = sorted([p.name for p in board.players])
        self.assertEqual(names, ["Bob", "Bob(1)"])

    def test_empty_names_default_to_gary(self):
        random.seed(42)
        board = Board(["", ""])
        names = sorted([p.name for p in board.players])
        self.assertEqual(names, ["Gary", "Gary(1)"])


class TestBoardStartGame(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.board = Board(["Alice", "Bob"])

    def test_start_game(self):
        state = self.board.start_game()
        self.assertEqual(state["state"], "waiting_for_guess")
        self.assertIsNotNone(state["current_card"])
        self.assertIn("desc", state["current_card"])
        # Value should be hidden
        self.assertNotIn("value", state["current_card"])

    def test_start_game_has_players(self):
        state = self.board.start_game()
        self.assertEqual(len(state["players"]), 2)

    def test_start_game_has_guesser_ranges(self):
        state = self.board.start_game()
        self.assertIsInstance(state["guesser_ranges"], list)
        self.assertTrue(len(state["guesser_ranges"]) > 0)


class TestBoardGuessing(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.board = Board(["Alice", "Bob"])
        self.board.start_game()

    def test_invalid_guess_index_negative(self):
        state = self.board.submit_guess(-1)
        # Should still be in game (not crashed)
        self.assertIn(
            state["state"], ["waiting_for_guess", "game_over"]
        )
        self.assertTrue(
            any("invalid" in m.lower() for m in state["messages"])
        )

    def test_invalid_guess_index_too_high(self):
        state = self.board.submit_guess(999)
        self.assertIn(
            state["state"], ["waiting_for_guess", "game_over"]
        )

    def test_correct_guess_awards_card(self):
        """Find the correct range and submit it."""
        card_value = self.board.current_card.value
        player = self.board.players[self.board.current_guesser]

        correct_index = None
        for i in range(player.num_ranges):
            r = player.guessed_range(i)
            if r[0] <= card_value <= r[1]:
                correct_index = i
                break

        initial_cards = player.num_cards
        state = self.board.submit_guess(correct_index)
        self.assertTrue(any("correctly" in m.lower() for m in state["messages"]))

        # Player should have gained a card
        self.assertEqual(player.num_cards, initial_cards + 1)

    def test_wrong_guess_advances_guesser(self):
        """Submit a definitely wrong guess and check guesser changes."""
        initial_guesser = self.board.current_guesser
        card_value = self.board.current_card.value
        player = self.board.players[initial_guesser]

        # Find a wrong range
        wrong_index = None
        for i in range(player.num_ranges):
            r = player.guessed_range(i)
            if not (r[0] <= card_value <= r[1]):
                wrong_index = i
                break

        if wrong_index is not None:
            state = self.board.submit_guess(wrong_index)
            # Guesser should have advanced
            self.assertNotEqual(self.board.current_guesser, initial_guesser)


class TestBoardGameFlow(unittest.TestCase):
    def test_full_game_to_completion(self):
        """Play a full game by always guessing index 0."""
        random.seed(123)
        board = Board(["Alice", "Bob"])
        state = board.start_game()

        moves = 0
        max_moves = 1000
        while state["state"] != "game_over" and moves < max_moves:
            state = board.submit_guess(0)
            moves += 1

        self.assertEqual(state["state"], "game_over")

    def test_game_over_deck_empty(self):
        """Force deck to empty and verify game ends."""
        random.seed(42)
        board = Board(["Alice", "Bob"])
        board.start_game()

        # Drain deck by playing through
        moves = 0
        while board.state != GameState.GAME_OVER and moves < 2000:
            board.submit_guess(0)
            moves += 1

        self.assertEqual(board.state, GameState.GAME_OVER)

    def test_previous_guesses_accumulate(self):
        """Wrong guesses should accumulate in previous_guesses."""
        random.seed(42)
        board = Board(["Alice", "Bob", "Charlie"])
        state = board.start_game()

        card_value = board.current_card.value
        player = board.players[board.current_guesser]

        # Find a wrong range
        wrong_index = None
        for i in range(player.num_ranges):
            r = player.guessed_range(i)
            if not (r[0] <= card_value <= r[1]):
                wrong_index = i
                break

        if wrong_index is not None:
            state = board.submit_guess(wrong_index)
            self.assertTrue(len(state["previous_guesses"]) > 0)


class TestBoardGetPlayerState(unittest.TestCase):
    def test_get_player_state(self):
        random.seed(42)
        board = Board(["Alice", "Bob"])
        board.start_game()

        player_name = board.players[0].name
        state = board.get_player_state(player_name)

        self.assertIn("my_hand", state)
        self.assertIn("is_my_turn", state)
        self.assertIsInstance(state["my_hand"], dict)


class TestNameCreation(unittest.TestCase):
    """Ported from original test_name_creation.py."""

    def test_same_name1(self):
        random.seed(42)
        a = Board(["Bob", "Bob"])
        self.assertEqual(
            sorted([p.name for p in a.players]), ["Bob", "Bob(1)"]
        )

    def test_random_order_same_name(self):
        random.seed(42)
        a = Board(["Bob", "Mike", "Tree", "Mike", "Willis", "Bob"])
        names = sorted([p.name for p in a.players])
        expected = sorted(["Bob", "Mike", "Tree", "Mike(1)", "Willis", "Bob(1)"])
        self.assertEqual(names, expected)

    def test_default_duplicate(self):
        random.seed(42)
        a = Board(["", "", "", "Gary(2)", ""])
        names = sorted([p.name for p in a.players])
        expected = sorted(["Gary", "Gary(1)", "Gary(2)", "Gary(2)(1)", "Gary(3)"])
        self.assertEqual(names, expected)


if __name__ == "__main__":
    unittest.main()
