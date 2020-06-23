#!/usr/bin/python3

"""
Abstraction of a player's hand

Current implementation: 
    - List of cards
    - List of ranges

"""

from card import Card
from typing import List, Tuple
import bisect, logging

class Hand:

    """
    Attributes:
        # cards     - List of cards
        # ranges    - List of ranges (tuples) that can be used for guesses)
        # num_cards - Number of cards in hand

    """

    def __init__(self):
        self.__cards     = []
        self.__ranges    = []
        self.__num_cards = 0

    @property
    def cards(self):
        return self.__cards

    @property
    def ranges(self):
        return self.__ranges
    
    @property
    def num_cards(self):
        return self.__num_cards


    # Adds card to Player's faceup cards if they guess correctly
    def gain_card(self, newCard):

        if self.__cards == []:
            self.__cards.append(newCard)
            self.__ranges.append((0, newCard.value))
            self.__ranges.append((newCard.value, 100.0))

        else:
            insertIndex = bisect.bisect(self.__cards, newCard)
            
            bisect.insort(self.__cards, newCard)
            self.__ranges[insertIndex] = (newCard.value, self.__ranges[insertIndex][1])

            if insertIndex != 0:
                self.__ranges.insert(insertIndex, (self.__ranges[insertIndex - 1][1] ,newCard.value))
            else:
                self.__ranges.insert(0, (0, newCard.value)) 


        self.__num_cards += 1

    def print_hand(self):
        for c in self.__cards:
            print(f"{c.desc} - {c.value}")



