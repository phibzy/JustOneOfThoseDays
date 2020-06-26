#!/usr/bin/python3

import unittest
from JustOneOfThoseDays.board import Board
from JustOneOfThoseDays.card import Card
from JustOneOfThoseDays.hand import Hand
from JustOneOfThoseDays.player import Player


class testRangeInsert(unittest.TestCase):
    
    def test_front_insert(self):
        b = Board([Player("Akerstache"), Player("Steven Wilton")])
        test_player = b.players[b.current_starter]

        self.assertEqual(test_player.hand.num_cards, 3, "Starting cards invalid")
        new_card = Card("Nothing happens", 0)

        test_player.hand.gain_card(new_card)

        self.assertEqual(len(test_player.hand.ranges), test_player.hand.num_cards, "Error - Number of ranges invalid")
        self.assertEqual(test_player.hand.cards[0], new_card, "Error - Card not inserted in front")


    def test_end_insert(self):
        p = Player("Damo")
        p.hand.gain_card(Card("Eat moldy cheese", 15))
        p.hand.gain_card(Card("Swallow pen ink", 38))
        p.hand.gain_card(Card("Hit in face with brick", 74))

        self.assertEqual(p.hand.num_cards, 3, "num_cards error")
        self.assertEqual(p.hand.ranges, [(0,15), (15,38), (38,74), (74, 100)], "End insert case 1")

        p.hand.gain_card(Card("Cut in half by samurai warrior", 90))

        self.assertEqual(p.hand.num_cards, 4, "num_cards error")
        self.assertEqual(p.hand.ranges, [(0,15), (15,38), (38,74), (74,90), (90, 100)], "End insert case 2")

        p.hand.gain_card(Card("Eaten", 100))

        self.assertEqual(p.hand.num_cards, 5, "num_cards error")
        self.assertEqual(p.hand.ranges, [(0,15), (15,38), (38,74), (74,90), (90, 100)], "End insert case 3")

    def test_middle_insert(self): 
        p = Player("Damo")
        p.hand.gain_card(Card("Eat moldy cheese", 15))
        p.hand.gain_card(Card("Swallow pen ink", 38))
        p.hand.gain_card(Card("Hit in face with brick", 74))

        self.assertEqual(p.hand.num_cards, 3, "num_cards error")
        self.assertEqual(p.hand.ranges, [(0,15), (15,38), (38,74), (74, 100)], "Middle insert case 1")

        p.hand.gain_card(Card("Flat tire", 42))
        self.assertEqual(p.hand.ranges, [(0,15), (15,38), (38, 42), (42,74), (74, 100)], "Middle insert case 2")

        p.hand.gain_card(Card("Writer's block", 40))
        self.assertEqual(p.hand.ranges, [(0,15), (15,38), (38,40), (40, 42), (42,74), (74, 100)], "Middle insert case 3")
        p.hand.gain_card(Card("Tester's block", 39))
        self.assertEqual(p.hand.ranges, [(0,15), (15,38), (38,39), (39,40), (40, 42), (42,74), (74, 100)], "Middle insert case 3")

    def test_duplicate_inserts(self):
        p = Player("Test Dummy")
        p.hand.gain_card(Card("Eat moldy cheese", 30))
        p.hand.gain_card(Card("Swallow pen ink", 20))
        p.hand.gain_card(Card("Hit in face with brick", 81))

        self.assertEqual(p.hand.num_cards, 3, "num_cards error")
        self.assertEqual(p.hand.ranges, [(0,20), (20,30), (30,81), (81, 100)], "Duplicate insert case 1")

        p.hand.gain_card(Card("Bitten by rat", 30))
        self.assertEqual(p.hand.num_cards, 4, "num_cards error")
        self.assertEqual(p.hand.ranges, [(0,20), (20,30), (30,81), (81, 100)], "Duplicate insert case 2")

        p.hand.gain_card(Card("Bitten by monkey", 30))
        self.assertEqual(p.hand.num_cards, 5, "num_cards error")
        self.assertEqual(p.hand.ranges, [(0,20), (20,30), (30,81), (81, 100)], "Duplicate insert case 3")

        p.hand.gain_card(Card("Devoured by giant spider", 81))
        self.assertEqual(p.hand.num_cards, 6, "num_cards error")
        self.assertEqual(p.hand.ranges, [(0,20), (20,30), (30,81), (81, 100)], "Duplicate insert case 4")

        p.hand.gain_card(Card("Devoured by giant spider", 81))
        self.assertEqual(p.hand.num_cards, 7, "num_cards error")
        self.assertEqual(p.hand.ranges, [(0,20), (20,30), (30,81), (81, 100)], "Duplicate insert case 5")

        p.hand.gain_card(Card("Devoured by giant spider", 81))
        self.assertEqual(p.hand.num_cards, 8, "num_cards error")
        self.assertEqual(p.hand.ranges, [(0,20), (20,30), (30,81), (81, 100)], "Duplicate insert case 6")

        p.hand.gain_card(Card("Devoured by giant spider", 81))
        self.assertEqual(p.hand.num_cards, 9, "num_cards error")
        self.assertEqual(p.hand.ranges, [(0,20), (20,30), (30,81), (81, 100)], "Duplicate insert case 7")
