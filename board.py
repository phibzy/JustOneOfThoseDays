#!/usr/bin/python3

"""
Represents the board of the game
Keeps track of the current game state
"""

from player import Player
from card import Card
from typing import List, Tuple
import random, re
import logging
import pprint

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
# logging.disable(logging.DEBUG)

class Board:

    STARTING_CARDS = 3

    # Game end conditions:
    # Player obtains 10 cards
    # Deck runs out of cards

    # TODO:
        # - Handle individual guesses (player.guess_range, define board method for guess handling)
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
        self.__players = players

        # Create the game deck here
        self.__deck = self.__initialise_deck()
        random.shuffle(self.__deck)
        
        # Choose starting player
        self.__num_players = len(self.__players)
        
        if self.__num_players < 2:
            raise Exception("Must have at least two players")

        # Give players their starting cards
        self.__initialise_player_cards()    

        # Shuffle players to have a random starter
        random.shuffle(self.__players)
        self.__current_starter = self.__players[0]
        
        # First guesser is the first starter
        self.__current_guesser = self.__current_starter

        self.__print_player_cards()

        self.__previous_guesses = list() # Thinking might put this in gamestate

    def draw_card(self):
        try:
            return self.__deck.pop(0)
        except IndexError:
            print("No cards left - game over!")

    # For debugging purposes - will remove later
    @property
    def deck(self):
        return self.__deck

    def __initialise_deck(self):
        cardRegex = re.compile(r"^(.*) (.*\d)$")
        deck = list()

        f1 = open("card_list.txt")
        for line in f1.readlines():
            mo = cardRegex.search(line)
            newCard = Card(mo.group(1), float(mo.group(2))) 
            deck.append(newCard)

        f1.close()
       
        return deck

    def __initialise_player_cards(self):
        # Each player draws 3 cards
        for player in self.__players:
            for _ in range(self.STARTING_CARDS):
                player.gain_card(self.draw_card())
   
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

    ##### DEBUG METHODS ######
    def __print_player_cards(self):
        for player in self.__players:
            print(f"Player {player.name}'s cards: ({player.num_cards} total)")
            for card in player.cards:
                print(f"{card.desc} - {card.value}")
        


