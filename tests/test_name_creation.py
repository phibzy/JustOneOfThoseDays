#!/usr/bin/python3

"""
  @author      : Chris Phibbs
  @created     : Tuesday Jun 23, 2020 10:38:47 AEST
  @file        : test_name_creation


  Tests for duplicate name handling

  IMPORTANT: TURN OFF PLAYER ORDER SHUFFLING BEFORE TESTING THIS

"""

import unittest
from JustOneOfThoseDays.board import Board
from JustOneOfThoseDays.player import Player

class TestNameCreation(unittest.TestCase):
    """ 

    Tests name creation module 
    Turn off player list shuffling to make sure this works

    """

    def test_same_name1(self):
        """ Single duplicate name case """
        a = Board([Player('Bob'), Player('Bob')])
        self.assertEqual(sorted(a.players), [Player('Bob'), Player('Bob(1)')], "Fails basic case")

    
    def test_random_order_same_name(self):
        """ Random order duplicate name case """
        names =   [ Player('Bob'),
                    Player('Mike'),
                    Player('Tree'),
                    Player('Mike'),
                    Player('Willis'),
                    Player('Bob')
                  ]

        a = Board(names)

        self.assertEqual(sorted(a.players), sorted([ 
                    Player('Bob'),
                    Player('Mike'),
                    Player('Tree'),
                    Player('Mike(1)'),
                    Player('Willis'),
                    Player('Bob(1)')
                  ])
        , "Fails random case")



    def all_same_name_with_extras(self):
        """ All same name, with some weird cases """
        a = Board([
                    Player('Bob'),
                    Player('Bob'),
                    Player('Bob(2)'),
                    Player('bob'),
                    Player('Bob'),
                    Player('Bob(3)'),
                    Player('Bob'),
                  ])

        self.assertEqual(sorted(a.players), sorted([ 
                    Player('Bob'),
                    Player('Bob(1)'),
                    Player('Bob(2)'),
                    Player('bob'),
                    Player('Bob(3)'),
                    Player('Bob(3)(1)'),
                    Player('Bob(4)'),
                  ])
        , "Fails random case")

    def test_default_duplicate(self):
        """ Single duplicate name case """
        a = Board([
                    Player(''),
                    Player(''),
                    Player(''),
                    Player('Gary(2)'),
                    Player(''),
                  ])

        self.assertEqual(sorted(a.players), sorted([ 
                    Player('Gary'),
                    Player('Gary(1)'),
                    Player('Gary(2)'),
                    Player('Gary(2)(1)'),
                    Player('Gary(3)'),
                  ])
        , "Fails random case")
