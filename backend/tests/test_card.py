"""
Tests for the Card class.
"""

import unittest

from backend.game.card import Card


class TestCard(unittest.TestCase):
    def test_creation(self):
        c = Card("Stub toe", 5.0)
        self.assertEqual(c.desc, "Stub toe")
        self.assertEqual(c.value, 5.0)

    def test_to_dict(self):
        c = Card("Stub toe", 5.0)
        self.assertEqual(c.to_dict(), {"desc": "Stub toe", "value": 5.0})

    def test_to_dict_hidden_value(self):
        c = Card("Stub toe", 5.0)
        self.assertEqual(c.to_dict(hide_value=True), {"desc": "Stub toe"})

    def test_less_than(self):
        c1 = Card("Low", 10.0)
        c2 = Card("High", 90.0)
        self.assertTrue(c1 < c2)
        self.assertFalse(c2 < c1)

    def test_equality(self):
        c1 = Card("Same", 50.0)
        c2 = Card("Same", 50.0)
        c3 = Card("Different", 50.0)
        self.assertEqual(c1, c2)
        self.assertNotEqual(c1, c3)


if __name__ == "__main__":
    unittest.main()
