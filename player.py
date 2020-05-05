#!/usr/bin/python3

"""
Class that represents player
Keeps track of what/how many cards they have

"""

from card import Card
from typing import List, Tuple
import bisect, logging

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(message)s")
logging.disable(logging.DEBUG)

class Player:

    # Attributes
    # cards     - a list of current Cards faceup on table
    # name      - the player's name
    # numCards  - an int with number of cards player has
    
    def __init__(self, name: str):
        self.__cards = []
        self.__name = name
        self.__num_cards = 0 # Cards given when board is initialised 

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
        logging.debug("".rjust(10,'-'))
        logging.debug(f"Player is {self.name}")
        logging.debug(f"New card is {newCard.desc} - {newCard.value}")

        logging.debug(f"Cardlist before insertion: {[(i.desc, i.value) for i in self.__cards]}")

        if self.__cards == []:
            self.__cards.append(newCard)

        else:
            bisect.insort(self.__cards, newCard)

        logging.debug(f"Cardlist before insertion: {[(i.desc, i.value) for i in self.__cards]}")

        self.__num_cards += 1

        if self.__num_cards == 10:
            print("You win!")

    # Will probably need a guess place
    def guess_range(self, desc: str) -> Tuple[float, float]:
        # Guess where in current card list new card will sit
        # If at ends of list, use range of (0,x) or (x, 101)

        pass

