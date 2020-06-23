#!/usr/bin/python3

"""
  @author      : Chris Phibbs
  @created     : Tuesday Jun 23, 2020 10:38:47 AEST
  @file        : test_name_creation


  Tests for duplicate name handling

  Cases:

  - 1 same name



"""

import unittest
from JOOTD.board import Board
from JOOTD.player import Player

class TestNameCreation(unittest.TestCase):
    """ 

    Tests name creation module 
    Turn off player list shuffling to make sure this works

    """

    def test_same_name1(self):
        """ Single duplicate name case """
        a = Board([Player('Bob'), Player('Bob')])
        self.assertEqual(a.players, [Player('Bob'), Player('Bob(1)')], "Fails basic case")

