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

        self.assertEqual(test_player.num_cards, 3, "Starting cards invalid")
        new_card = Card("Nothing happens", 0)

        test_player.gain_card(new_card)

        self.assertEqual(test_player.num_ranges, test_player.num_cards, "Error - Number of ranges invalid")
        self.assertEqual(test_player.card_index(0), new_card, "Error - Card not inserted in front")


    def test_end_insert(self):
        p = Player("Damo")
        p.gain_card(Card("Eat moldy cheese", 15))
        p.gain_card(Card("Swallow pen ink", 38))
        p.gain_card(Card("Hit in face with brick", 74))

        self.assertEqual(p.num_cards, 3, "num_cards error")
        self.assertEqual(p.ranges, [(0,15), (15,38), (38,74), (74, 100)], "End insert case 1")

        p.gain_card(Card("Cut in half by samurai warrior", 90))

        self.assertEqual(p.num_cards, 4, "num_cards error")
        self.assertEqual(p.ranges, [(0,15), (15,38), (38,74), (74,90), (90, 100)], "End insert case 2")

        p.gain_card(Card("Eaten", 100))

        self.assertEqual(p.num_cards, 5, "num_cards error")
        self.assertEqual(p.ranges, [(0,15), (15,38), (38,74), (74,90), (90, 100)], "End insert case 3")

    def test_middle_insert(self): 
        p = Player("Damo")
        p.gain_card(Card("Eat moldy cheese", 15))
        p.gain_card(Card("Swallow pen ink", 38))
        p.gain_card(Card("Hit in face with brick", 74))

        self.assertEqual(p.num_cards, 3, "num_cards error")
        self.assertEqual(p.ranges, [(0,15), (15,38), (38,74), (74, 100)], "Middle insert case 1")

        p.gain_card(Card("Flat tire", 42))
        self.assertEqual(p.ranges, [(0,15), (15,38), (38, 42), (42,74), (74, 100)], "Middle insert case 2")

        p.gain_card(Card("Writer's block", 40))
        self.assertEqual(p.ranges, [(0,15), (15,38), (38,40), (40, 42), (42,74), (74, 100)], "Middle insert case 3")

        p.gain_card(Card("Tester's block", 39))
        self.assertEqual(p.ranges, [(0,15), (15,38), (38,39), (39,40), (40, 42), (42,74), (74, 100)], "Middle insert case 3")

    def test_duplicate_inserts(self):
        p = Player("Test Dummy")
        p.gain_card(Card("Eat moldy cheese", 30))
        p.gain_card(Card("Swallow pen ink", 20))
        p.gain_card(Card("Hit in face with brick", 81))

        self.assertEqual(p.num_cards, 3, "num_cards error")
        self.assertEqual(p.ranges, [(0,20), (20,30), (30,81), (81, 100)], "Duplicate insert case 1")

        p.gain_card(Card("Bitten by rat", 30))
        self.assertEqual(p.num_cards, 4, "num_cards error")
        self.assertEqual(p.ranges, [(0,20), (20,30), (30,81), (81, 100)], "Duplicate insert case 2")

        p.gain_card(Card("Bitten by monkey", 30))
        self.assertEqual(p.num_cards, 5, "num_cards error")
        self.assertEqual(p.ranges, [(0,20), (20,30), (30,81), (81, 100)], "Duplicate insert case 3")

        p.gain_card(Card("Devoured by giant spider", 81))
        self.assertEqual(p.num_cards, 6, "num_cards error")
        self.assertEqual(p.ranges, [(0,20), (20,30), (30,81), (81, 100)], "Duplicate insert case 4")

        p.gain_card(Card("Devoured by giant spider", 81))
        self.assertEqual(p.num_cards, 7, "num_cards error")
        self.assertEqual(p.ranges, [(0,20), (20,30), (30,81), (81, 100)], "Duplicate insert case 5")

        p.gain_card(Card("Devoured by giant spider", 81))
        self.assertEqual(p.num_cards, 8, "num_cards error")
        self.assertEqual(p.ranges, [(0,20), (20,30), (30,81), (81, 100)], "Duplicate insert case 6")

        p.gain_card(Card("Devoured by giant spider", 81))
        self.assertEqual(p.num_cards, 9, "num_cards error")
        self.assertEqual(p.ranges, [(0,20), (20,30), (30,81), (81, 100)], "Duplicate insert case 7")

    def test_insert_limited_original_ranges(self):
        p = Player("Test Dummy2")
        p.gain_card(Card("Meh", 0))
        self.assertEqual(p.num_cards, 1, "num_cards error")
        self.assertEqual(p.ranges, [(0, 100)], "Default range case 1")

        p.gain_card(Card("AAH", 100))
        self.assertEqual(p.num_cards, 2, "num_cards error")
        self.assertEqual(p.ranges, [(0, 100)], "Default range case 2")

        p.gain_card(Card("Middle range card", 50))
        self.assertEqual(p.num_cards, 3, "num_cards error")
        self.assertEqual(p.ranges, [(0, 50), (50,100)], "Default range case 3")

        p.gain_card(Card("AAH2", 100))
        self.assertEqual(p.num_cards, 4, "num_cards error")
        self.assertEqual(p.ranges, [(0, 50), (50,100)], "Default range case 3")

    def test_weird_duplicate_range_front(self):
        p = Player("Test Dummy3")
        p.gain_card(Card("Unwilling subject of love song", 62))
        self.assertEqual(p.num_cards, 1, "num_cards error")
        self.assertEqual(p.ranges, [(0, 62), (62,100)], "Weird duplicate range case 1")

        p.gain_card(Card("Unwilling subject of love song", 62))
        self.assertEqual(p.num_cards, 2, "num_cards error")
        self.assertEqual(p.ranges, [(0, 62), (62,100)], "Weird duplicate range case 2")

        p.gain_card(Card("Unwilling subject of love song", 62))
        self.assertEqual(p.num_cards, 3, "num_cards error")
        self.assertEqual(p.ranges, [(0, 62), (62,100)], "Weird duplicate range case 3")

        p.gain_card(Card("Unwilling subject of love song", 62))
        self.assertEqual(p.num_cards, 4, "num_cards error")
        self.assertEqual(p.ranges, [(0, 62), (62,100)], "Weird duplicate range case 4")

        p.gain_card(Card("Unwilling subject of love song", 62))
        self.assertEqual(p.num_cards, 5, "num_cards error")
        self.assertEqual(p.ranges, [(0, 62), (62,100)], "Weird duplicate range case 5")

        p.gain_card(Card("Super sleepiness", 43))
        self.assertEqual(p.num_cards, 6, "num_cards error")
        self.assertEqual(p.ranges, [(0, 43), (43, 62), (62,100)], "Weird duplicate range case 5")

        p.gain_card(Card("Super sleepiness", 43))
        self.assertEqual(p.num_cards, 7, "num_cards error")
        self.assertEqual(p.ranges, [(0, 43), (43, 62), (62,100)], "Weird duplicate range case 5")

        #### CRITICAL PART OF TEST #####
        p.gain_card(Card("Break stuff", 50))
        self.assertEqual(p.num_cards, 8, "num_cards error")
        self.assertEqual(p.ranges, [(0, 43), (43, 50), (50, 62), (62,100)], "Weird duplicate range case 5")

    def test_weird_duplicate_range_front2(self):
        p = Player("Test Dummy3")
        p.gain_card(Card("Unwilling subject of love song", 62))
        self.assertEqual(p.num_cards, 1, "num_cards error")
        self.assertEqual(p.ranges, [(0, 62), (62,100)], "Weird duplicate range case 1")

        p.gain_card(Card("Unwilling subject of love song", 62))
        self.assertEqual(p.num_cards, 2, "num_cards error")
        self.assertEqual(p.ranges, [(0, 62), (62,100)], "Weird duplicate range case 2")

        p.gain_card(Card("Unwilling subject of love song", 62))
        self.assertEqual(p.num_cards, 3, "num_cards error")
        self.assertEqual(p.ranges, [(0, 62), (62,100)], "Weird duplicate range case 3")

        p.gain_card(Card("Unwilling subject of love song", 62))
        self.assertEqual(p.num_cards, 4, "num_cards error")
        self.assertEqual(p.ranges, [(0, 62), (62,100)], "Weird duplicate range case 4")

        p.gain_card(Card("Unwilling subject of love song", 62))
        self.assertEqual(p.num_cards, 5, "num_cards error")
        self.assertEqual(p.ranges, [(0, 62), (62,100)], "Weird duplicate range case 5")

        p.gain_card(Card("Super sleepiness", 43))
        self.assertEqual(p.num_cards, 6, "num_cards error")
        self.assertEqual(p.ranges, [(0, 43), (43, 62), (62,100)], "Weird duplicate range case 5")

        p.gain_card(Card("Super sleepiness", 43))
        self.assertEqual(p.num_cards, 7, "num_cards error")
        self.assertEqual(p.ranges, [(0, 43), (43, 62), (62,100)], "Weird duplicate range case 5")

        #### CRITICAL PART OF TEST #####
        p.gain_card(Card("Break stuff", 73))
        self.assertEqual(p.num_cards, 8, "num_cards error")
        self.assertEqual(p.ranges, [(0, 43), (43, 62), (62, 73), (73, 100)], "Weird duplicate range case 5")

    def test_weird_duplicate_range_back(self):
        p = Player("Test Dummy3")
        p.gain_card(Card("Unwilling subject of love song", 62))
        self.assertEqual(p.num_cards, 1, "num_cards error")
        self.assertEqual(p.ranges, [(0, 62), (62,100)], "Weird duplicate range case 1")

        p.gain_card(Card("Unwilling subject of love song", 62))
        self.assertEqual(p.num_cards, 2, "num_cards error")
        self.assertEqual(p.ranges, [(0, 62), (62,100)], "Weird duplicate range case 2")

        p.gain_card(Card("Unwilling subject of love song", 62))
        self.assertEqual(p.num_cards, 3, "num_cards error")
        self.assertEqual(p.ranges, [(0, 62), (62,100)], "Weird duplicate range case 3")

        p.gain_card(Card("Unwilling subject of love song", 62))
        self.assertEqual(p.num_cards, 4, "num_cards error")
        self.assertEqual(p.ranges, [(0, 62), (62,100)], "Weird duplicate range case 4")

        p.gain_card(Card("Unwilling subject of love song", 62))
        self.assertEqual(p.num_cards, 5, "num_cards error")
        self.assertEqual(p.ranges, [(0, 62), (62,100)], "Weird duplicate range case 5")

        p.gain_card(Card("Super sleepiness", 75))
        self.assertEqual(p.num_cards, 6, "num_cards error")
        self.assertEqual(p.ranges, [(0, 62), (62, 75), (75, 100)], "Weird duplicate range case 5")

        p.gain_card(Card("Super sleepiness", 75))
        self.assertEqual(p.num_cards, 7, "num_cards error")
        self.assertEqual(p.ranges, [(0, 62), (62, 75), (75, 100)], "Weird duplicate range case 5")

