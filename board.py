#!/usr/bin/python3

"""
Represents the board of the game
Keeps track of the current game state
"""

from player import Player
from card import Card
from typing import List, Tuple
import re
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
# logging.disable(logging.DEBUG)

class Board:

    # Attributes
    # players       - A list of Players, all the people playing the game
    # deck          - A list of Cards
    # current_starter - The first player guessing for a particular round
    # current_guesser - The current Player guessing
    # num_players     - The number of Players

    # May want dict keeping track of scores, as the board object is
    # what will ultimately signal end of game

    # Initialiser/constructor
    def __init__(self):
        self.__players = self.__initialise_players()

        # Create the game deck here
        self.__deck = self.__initialise_deck()
        
        # Choose starting player
        self.__current_starter = None#self.players[0]

        # First guesser is the first starter
        self.__current_guesser = None#self.players[0]

        self.__num_players = len(self.__players)

    def draw_card(self):
        pass

    @property
    def deck(self) -> List[Tuple[str, int]]:
        returnDeck = [(i.desc, i.value) for i in self.__deck]

        return returnDeck

    def __initialise_deck(self):
        cardRegex = re.compile(r"^(.*) (.*\d)$")
        deck = list()

        f1 = open("card_list.txt")
        for line in f1.readlines():
            mo = cardRegex.search(line)
            newCard = Card(mo.group(1), mo.group(2)) 
            deck.append(newCard)

        f1.close()
       
        return deck

    def __initialise_players(self):
        return list()
    
    def next_guesser(self):
        

    def next_turn(self):
        pass

