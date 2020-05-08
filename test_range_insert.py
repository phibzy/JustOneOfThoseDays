#!/usr/bin/python3

import unittest
from board import Board
from player import Player
from card import Card

class testRangeInsert(unittest.TestCase):
    
    #TODO: Test inserting into ranges at the end (e.g. with 100)


    def testFrontInsert(self):
        b = Board([Player("Akerstache")])
        testPlayer = b.current_starter
        
        self.assertEqual(testPlayer.ranges, testPlayer.num_cards + 1, "Error - Number of ranges invalid")

        newCard = Card("Nothing happens", 0)

        testPlayer.gain_card(newCard)

        self.assertEqual(testPlayer.ranges, testPlayer.num_cards + 1, "Error - Number of ranges invalid")
        self.assertEqual(testPlayer.cards[0], newCard, "Error - Card not inserted in front")
        self.assertEqual(testPlayer.ranges[0], (0,0), "Error - Range not 0,0")
        self.assertEqual(testPlayer.ranges[1][0], 0, "Error - First element of next tuple not changed")




