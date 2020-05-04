#!/usr/bin/python3

from board import Board
from player import Player
import pprint

players = [ Player("Damo"), 
            Player("Darren")
          ]

board = Board(players)
print(pprint.pformat([(i.desc, i.value) for i in board.deck]))
