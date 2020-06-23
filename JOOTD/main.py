#!/usr/bin/python3

from board import Board
from player import Player
import pprint

players = [ 
            Player("Bob"),
            Player("Bob"),
            Player("Bob"),
            Player("Bob"),
            Player("Bob"),
            Player("Bob(4)"),
            Player("Fred")
          ]

board = Board(players)
board.start_game()
