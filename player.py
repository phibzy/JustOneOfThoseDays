#!/usr/bin/python3

"""
Class that represents player
Keeps track of what/how many cards they have

"""

from card import Card
from typing import List, Tuple
import bisect, logging

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(message)s")
#logging.disable(logging.DEBUG)

class Player:

    # Attributes
    # cards     - a list of current Cards faceup on table
    # name      - the player's name
    # numCards  - an int with number of cards player has

    #TODO: Gamestate passed into guess_range, player gets options from gamestate
           # Not sure if this is the best way though arrrrgghghghghgh
    
    def __init__(self, name: str):
        self.__cards  = []
        self.__ranges = [] # Contains valid ranges for guessing
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

    @property
    def ranges(self):
        return self.__ranges

    # Adds card to Player's faceup cards if they guess correctly
    def gain_card(self, newCard):
        logging.debug("".rjust(10,'-'))
        logging.debug(f"Player is {self.name}")
        logging.debug(f"New card is {newCard.desc} - {newCard.value}")

        logging.debug(f"Cardlist before insertion: {[(i.desc, i.value) for i in self.__cards]}")

        if self.__cards == []:
            self.__cards.append(newCard)
            self.__ranges.append((0, newCard.value))
            self.__ranges.append((newCard.value, 100.0))

        else:
            insertIndex = bisect.bisect(self.__cards, newCard)
            
            logging.debug(f"insertIndex is: {insertIndex}")
            logging.debug(f"Ranges before insertion: {self.__ranges}")

            bisect.insort(self.__cards, newCard)
            self.__ranges[insertIndex] = (newCard.value, self.__ranges[insertIndex][1])

            if insertIndex != 0:
                self.__ranges.insert(insertIndex, (self.__ranges[insertIndex - 1][1] ,newCard.value))
            else:
                self.__ranges.insert(0, (0, newCard.value)) 

            logging.debug(f"Ranges after insertion: {self.__ranges}")

        logging.debug(f"Cardlist after insertion: {[(i.desc, i.value) for i in self.__cards]}")

        self.__num_cards += 1

        if self.__num_cards == 10:
            print("You win!")

    # May be best to seperate this from rest of class definition? - means others can't rewrite ranges etc.
    # Will probably need a guess place
    # Possibly have board with an orderedDict that checks if player guess was one of the valid ranges
    def guess_range(self, desc: str) -> Tuple[float, float]:
        # Guess where in current card list new card will sit
        # If at ends of list, use range of (0,x) or (x, 100)
        # Need checks for valid ranges as well - have the board use a hash table for that
        print("Choose from the following:")

        """
        ### HOW I'LL DO THIS ###
        
        Board prints out list of options, player enters numbered option

        Will be better this way if we want to run AIs etc.


        """
        # Dummy one could be guess range 0 <= first_card.val everytime


        pass












