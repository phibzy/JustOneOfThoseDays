#!/usr/bin/python3

"""
  @author      : Chris Phibbs
  @created     : Tuesday Jun 23, 2020 10:38:47 AEST
  @file        : test_name_creation


  Tests for duplicate name handling

  Cases:

  - 1 same name
  - 



"""

import unittest
from board import Board
import sys
import io

class NullIO(io.StringIO):
    def write(self, txt):
       pass

class testNameCreation(unittest.TestCase):

    # Turn off NumPlayer error to get this to work
    # a = Board([])

    def testSameName1(self):
        a = Board(['Bob', 'Bob'])
        self.assertEqual(a.players, ['Bob', 'Bob(1)'], "Fails basic case")
        






