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
        self.__boundaries = dict()
        self.__cards      = []
        self.__ranges     = []
        self.__num_cards  = 0

    @property
    def boundaries(self):
        return self.__boundaries

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
    def gain_card(self, new_card):

        if self.__cards == []:
            self.__cards.append(new_card)
            self.__ranges.append((0, new_card.value))
            self.__ranges.append((new_card.value, 100.0))
            self.__boundaries[new_card.value] = 1
            self.__boundaries[0] = 1
            self.__boundaries[100] = 1

        else:
            insert_index = bisect.bisect(self.__cards, new_card)
            
            bisect.insort(self.__cards, new_card)

            if new_card.value not in self.__boundaries:

                self.__ranges[insert_index] = (new_card.value, self.__ranges[insert_index][1])

                if insert_index != 0:
                    self.__ranges.insert(insert_index, (self.__ranges[insert_index - 1][1] ,new_card.value))
                else:
                    self.__ranges.insert(0, (0, new_card.value)) 

                self.__boundaries[new_card.value] = 1


        self.__num_cards += 1

    def print_hand(self):
        for c in self.__cards:
            print(f"{c.desc} - {c.value}")



