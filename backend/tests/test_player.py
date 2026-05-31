"""
Tests for the Player class.
"""

import unittest

from backend.game.card import Card
from backend.game.player import Player


class TestPlayer(unittest.TestCase):
    def test_creation(self):
        p = Player("Alice")
        self.assertEqual(p.name, "Alice")
        self.assertEqual(p.num_cards, 0)

    def test_name_setter(self):
        p = Player("Alice")
        p.name = "Bob"
        self.assertEqual(p.name, "Bob")

    def test_gain_card(self):
        p = Player("Alice")
        p.gain_card(Card("Test", 50))
        self.assertEqual(p.num_cards, 1)

    def test_to_dict_basic(self):
        p = Player("Alice")
        d = p.to_dict()
        self.assertEqual(d, {"name": "Alice", "num_cards": 0, "is_cpu": False})

    def test_to_dict_cpu(self):
        p = Player("Robo", is_cpu=True)
        d = p.to_dict()
        self.assertEqual(d, {"name": "Robo", "num_cards": 0, "is_cpu": True})

    def test_to_dict_with_hand(self):
        p = Player("Alice")
        p.gain_card(Card("Test", 50))
        d = p.to_dict(include_hand=True)
        self.assertEqual(d["name"], "Alice")
        self.assertEqual(d["num_cards"], 1)
        self.assertIn("hand", d)
        self.assertEqual(d["hand"]["num_cards"], 1)

    def test_equality(self):
        p1 = Player("Alice")
        p2 = Player("Alice")
        p3 = Player("Bob")
        self.assertEqual(p1, p2)
        self.assertNotEqual(p1, p3)

    def test_less_than(self):
        p1 = Player("Alice")
        p2 = Player("Bob")
        self.assertTrue(p1 < p2)

    def test_ranges(self):
        p = Player("Alice")
        p.gain_card(Card("A", 50))
        self.assertEqual(p.ranges, [(0, 50), (50, 100)])
        self.assertEqual(p.num_ranges, 2)

    def test_guessed_range(self):
        p = Player("Alice")
        p.gain_card(Card("A", 50))
        self.assertEqual(p.guessed_range(0), (0, 50))
        self.assertEqual(p.guessed_range(1), (50, 100))


if __name__ == "__main__":
    unittest.main()
