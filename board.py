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

    # Game end conditions:
    # Player obtains 10 cards
    # Deck runs out of cards

    # TODO:
        # - Give players starting cards
        # - Handle each round
        # - Handling previous guesses properly

    # Attributes
    # current_guesser  - The current Player guessing
    # current_leader   - Current player in the lead - tentative
    # current_starter  - The first player guessing for a particular round
    # deck             - A list of Cards
    # num_players      - The number of Players
    # players          - A list of Players, all the people playing the game
    # previous_guesses - List of tuples containing range guesses of other players for current round
        #Note: To handle end ranges, do (0,x) and (x, 101)

    # May want dict keeping track of scores, as the board object is
    # what will ultimately signal end of game

    # Initialiser/constructor
    def __init__(self, players):

        # Players get passed in to class    
        self.__players = players#self.__initialise_players()

        # Create the game deck here
        self.__deck = self.__initialise_deck()
        
        # Choose starting player
        self.__current_starter = None#self.players[0]

        # First guesser is the first starter
        self.__current_guesser = None#self.players[0]

        self.__num_players = len(self.__players)

        self.__previous_guesses = list()

    def draw_card(self):
        try:
            return self.__deck.pop(0)
        except IndexError:
            print("No cards left - game over!")

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

    # Not used for now
    def __initialise_players(self):
        return list()
   
    # Returns None when everyone has had a turn guessing
    def next_guesser(self):
        self.__current_guesser += 1
        self.__current_guesser = self.__current_guesser % self.__num_players
        
        if (self.__current_guesser != self.__current_starter):
            return self.__players[self.__current_guesser]

    def next_turn(self):
        self.__current_starter += 1
        self.__current_starter = self.__current_starter % self.__num_players

        return self.__players[self.__current_starter]

