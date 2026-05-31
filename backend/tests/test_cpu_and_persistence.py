"""
Tests for CPU players and on-disk game persistence.
"""

import os
import random
import unittest

from backend.game.board import Board, GameState
from backend.game_manager import GameManager, GameSession


class TestCpuPlayers(unittest.TestCase):
    def test_cpu_flag_assigned(self):
        random.seed(1)
        board = Board(["Human", "Robo"], cpu_flags=[False, True])
        cpu_players = [p for p in board.players if p.is_cpu]
        human_players = [p for p in board.players if not p.is_cpu]
        self.assertEqual(len(cpu_players), 1)
        self.assertEqual(len(human_players), 1)
        self.assertEqual(cpu_players[0].name, "Robo")

    def test_advance_stops_on_human(self):
        random.seed(1)
        board = Board(["Human", "Robo"], cpu_flags=[False, True])
        board.start_game()
        board.advance_cpu_turns()
        # If still waiting for a guess, it must be the human's turn.
        if board.state == GameState.WAITING_FOR_GUESS:
            self.assertFalse(board.players[board.current_guesser].is_cpu)

    def test_all_cpu_game_completes(self):
        random.seed(7)
        board = Board(["Robo1", "Robo2"], cpu_flags=[True, True])
        board.start_game()
        state = board.advance_cpu_turns()
        # A fully-CPU game should play itself to completion.
        self.assertEqual(state["state"], "game_over")

    def test_choose_guess_in_range(self):
        random.seed(3)
        board = Board(["Robo1", "Robo2"], cpu_flags=[True, True])
        player = board.players[0]
        idx = board._cpu_choose_guess(player)
        self.assertGreaterEqual(idx, 0)
        self.assertLess(idx, player.num_ranges)


class TestPersistence(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join(
            os.path.dirname(__file__), "_test_state.json"
        )
        if os.path.exists(self.path):
            os.remove(self.path)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_session_roundtrip(self):
        random.seed(5)
        session = GameSession("abc123", ["Alice", "Robo"], [False, True])
        session.start()
        data = session.serialize()
        restored = GameSession.from_serialized(data)

        self.assertEqual(restored.game_id, session.game_id)
        self.assertEqual(restored.player_tokens, session.player_tokens)
        self.assertEqual(
            [p.name for p in restored.board.players],
            [p.name for p in session.board.players],
        )
        self.assertEqual(
            [p.is_cpu for p in restored.board.players],
            [p.is_cpu for p in session.board.players],
        )
        self.assertEqual(restored.board.state, session.board.state)
        self.assertEqual(restored.board.num_cards, session.board.num_cards)

    def test_manager_survives_restart(self):
        random.seed(9)
        manager = GameManager(storage_path=self.path)
        session = manager.create_game("game1", ["Alice", "Bob"], [False, False])
        session.start()
        manager.save()

        # Simulate a server restart by constructing a fresh manager.
        restored = GameManager(storage_path=self.path)
        self.assertIn("game1", restored.list_games())
        reloaded = restored.get_game("game1")
        self.assertIsNotNone(reloaded)
        self.assertEqual(
            sorted(reloaded.player_tokens.keys()),
            sorted(session.player_tokens.keys()),
        )
        # A previously issued token still resolves to the right player.
        for token, name in session.token_to_player.items():
            self.assertEqual(reloaded.get_player_by_token(token), name)

    def test_corrupt_state_ignored(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("not valid json {")
        manager = GameManager(storage_path=self.path)
        self.assertEqual(manager.list_games(), [])


if __name__ == "__main__":
    unittest.main()
