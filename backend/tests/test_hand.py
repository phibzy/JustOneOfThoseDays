"""
Tests for the Hand class.
"""

import unittest

from backend.game.card import Card
from backend.game.hand import Hand


class TestHand(unittest.TestCase):
    def test_initial_state(self):
        h = Hand()
        self.assertEqual(h.num_cards, 0)
        self.assertEqual(h.num_ranges, 1)
        self.assertEqual(h.ranges, [(0, 100)])

    def test_gain_card(self):
        h = Hand()
        h.gain_card(Card("Test", 50))
        self.assertEqual(h.num_cards, 1)
        self.assertEqual(h.num_ranges, 2)
        self.assertEqual(h.ranges, [(0, 50), (50, 100)])

    def test_get_cards_list(self):
        h = Hand()
        h.gain_card(Card("Test", 50))
        cards = h.get_cards_list()
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0], {"desc": "Test", "value": 50})

    def test_get_ranges_list(self):
        h = Hand()
        result = h.get_ranges_list()
        self.assertEqual(result, [{"index": 1, "low": 0, "high": 100}])

    def test_get_ranges_list_after_card(self):
        h = Hand()
        h.gain_card(Card("Mid", 50))
        result = h.get_ranges_list()
        self.assertEqual(
            result,
            [
                {"index": 1, "low": 0, "high": 50},
                {"index": 2, "low": 50, "high": 100},
            ],
        )

    def test_to_dict(self):
        h = Hand()
        h.gain_card(Card("Test", 50))
        d = h.to_dict()
        self.assertEqual(d["num_cards"], 1)
        self.assertEqual(d["num_ranges"], 2)
        self.assertEqual(len(d["cards"]), 1)
        self.assertEqual(len(d["ranges"]), 2)

    def test_guessed_range(self):
        h = Hand()
        h.gain_card(Card("Test", 50))
        self.assertEqual(h.guessed_range(0), (0, 50))
        self.assertEqual(h.guessed_range(1), (50, 100))

    def test_card_index(self):
        h = Hand()
        c = Card("Test", 50)
        h.gain_card(c)
        self.assertEqual(h.card_index(0), c)


class TestRangeInsert(unittest.TestCase):
    """Ported from original test_range_insert.py for the refactored Hand/Player."""

    def test_front_insert(self):
        h = Hand()
        h.gain_card(Card("A", 20))
        h.gain_card(Card("B", 40))
        h.gain_card(Card("C", 60))
        new_card = Card("Nothing happens", 0)
        h.gain_card(new_card)
        self.assertEqual(h.card_index(0), new_card)

    def test_end_insert(self):
        h = Hand()
        h.gain_card(Card("A", 15))
        h.gain_card(Card("B", 38))
        h.gain_card(Card("C", 74))
        self.assertEqual(h.ranges, [(0, 15), (15, 38), (38, 74), (74, 100)])

        h.gain_card(Card("D", 90))
        self.assertEqual(h.ranges, [(0, 15), (15, 38), (38, 74), (74, 90), (90, 100)])

        h.gain_card(Card("E", 100))
        self.assertEqual(h.ranges, [(0, 15), (15, 38), (38, 74), (74, 90), (90, 100)])

    def test_middle_insert(self):
        h = Hand()
        h.gain_card(Card("A", 15))
        h.gain_card(Card("B", 38))
        h.gain_card(Card("C", 74))
        self.assertEqual(h.ranges, [(0, 15), (15, 38), (38, 74), (74, 100)])

        h.gain_card(Card("D", 42))
        self.assertEqual(
            h.ranges, [(0, 15), (15, 38), (38, 42), (42, 74), (74, 100)]
        )

    def test_duplicate_inserts(self):
        h = Hand()
        h.gain_card(Card("A", 30))
        h.gain_card(Card("B", 20))
        h.gain_card(Card("C", 81))
        self.assertEqual(h.ranges, [(0, 20), (20, 30), (30, 81), (81, 100)])

        h.gain_card(Card("D", 30))
        self.assertEqual(h.num_cards, 4)
        self.assertEqual(h.ranges, [(0, 20), (20, 30), (30, 81), (81, 100)])

    def test_insert_limited_original_ranges(self):
        h = Hand()
        h.gain_card(Card("Meh", 0))
        self.assertEqual(h.ranges, [(0, 100)])

        h.gain_card(Card("AAH", 100))
        self.assertEqual(h.ranges, [(0, 100)])

        h.gain_card(Card("Middle", 50))
        self.assertEqual(h.ranges, [(0, 50), (50, 100)])


if __name__ == "__main__":
    unittest.main()
