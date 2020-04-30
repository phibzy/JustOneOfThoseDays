#!/usr/bin/python3

"""
Represents the board of the game
Keeps track of the current game state
"""

from player import Player

class Board:

    # Attributes
    # players       - A list of Players, all the people playing the game
    # deck          - A list of Cards
    # currentPlayer - The current Player for a given turn

    # Initialiser/constructor
    def __init__(self, players, deck):
        self.players = players

        # Create the game deck here
        self.deck = deck

    def draw_card(self):
        pass

    
    def next_turn(self):
        pass

    def next_guesser(self):
        pass
