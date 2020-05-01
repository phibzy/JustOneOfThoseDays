#!/usr/bin/python3

"""
Represents the board of the game
Keeps track of the current game state
"""

from player import Player
from card import Card
import re
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
# logging.disable(logging.DEBUG)

class Board:

    # Note - for python OO, _ before variable name is used to denote private attributes

    # Pythonic way to do getters/setters is using "property"


    # Attributes
    # players       - A list of Players, all the people playing the game
    # deck          - A list of Cards
    # currentPlayer - The current Player for a given turn

    # Initialiser/constructor
    def __init__(self):
        self.__players = self.initialise_players()

        # Create the game deck here
        self.__deck = self.initialise_deck()
        
        # Choose starting player
        self.__current_player = None#self.players[0]

    def draw_card(self):
        pass

    @property
    def deck(self):
        returnDeck = [(i.desc, i.value) for i in self.__deck]

        return returnDeck

    def initialise_deck(self):
        cardRegex = re.compile(r"^(.*) (.*\d)$")
        deck = list()

        f1 = open("card_list.txt")
        for line in f1.readlines():
            mo = cardRegex.search(line)
            newCard = Card(mo.group(1), mo.group(2)) 
            deck.append(newCard)
       
        return deck

    def initialise_players(self):
        return list()
    
    def next_guesser(self):
        pass

    def next_turn(self):
        pass

