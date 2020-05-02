#!/usr/bin/python3

"""
Class that represents player
Keeps track of what/how many cards they have

"""

from card import Card
from typing import List, Tuple

class Player:

    # Attributes
    # cards     - a list of current Cards faceup on table
    # name      - the player's name
    # numCards  - an int with number of cards player has
    
    def __init__(self, name: str, cards):
        self.__cards = cards
        self.__name = name
        self.__num_cards = 3 # Each player starts with three cards
                          # Possibly change this to 0 depending on how first card is handled

    # Our getter methods
    @property
    def cards(self):
        return self.__cards 

    @property
    def name(self) -> str:
        return self.__name

    @property
    def num_cards(self) -> int:
        return self.__num_cards

    # Adds card to Player's faceup cards if they guess correctly
    def gain_card(self, newCard):
        self.__cards.append(newCard) # Want to insert it in order
        self.__num_cards += 1

        if self.__num_cards == 10:
            print("You win!")

    # Will probably need a guess place
    def guess_range(self, desc: str) -> Tuple[float, float]:
        # Guess where in current card list new card will sit
        # If at ends of list, use range of (0,x) or (x, 101)


        pass
