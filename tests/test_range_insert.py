#!/usr/bin/python3

import unittest
from JustOneOfThoseDays.board import Board
from JustOneOfThoseDays.player import Player
from JustOneOfThoseDays.card import Card

class testRangeInsert(unittest.TestCase):
    
    #TODO: Test inserting into ranges at the end (e.g. with 100)


    def testFrontInsert(self):
        b = Board([Player("Akerstache"), Player("Steven Wilton")])
        testPlayer = b.players[b.current_starter]
        
        self.assertEqual(len(testPlayer.hand.ranges), testPlayer.hand.num_cards + 1, "Error - Number of ranges invalid")

        newCard = Card("Nothing happens", 0)

        testPlayer.hand.gain_card(newCard)

        self.assertEqual(len(testPlayer.hand.ranges), testPlayer.hand.num_cards + 1, "Error - Number of ranges invalid")
        self.assertEqual(testPlayer.hand.cards[0], newCard, "Error - Card not inserted in front")
        self.assertEqual(testPlayer.hand.ranges[0], (0,0), "Error - Range not 0,0")
        self.assertEqual(testPlayer.hand.ranges[1][0], 0, "Error - First element of next tuple not changed")




