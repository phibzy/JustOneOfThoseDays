#!/usr/bin/python3

"""
Class for representing cards in the game

"""

class Card:
    # Attributes
    # desc  - A description of the unfortunate scenario on said card
    # value - The misery index value assigned to this card (float)

    def __init__(self, desc: str, value: float):
        self.__desc  = desc
        self.__value = value

    # Define less than operator for card - just like in C++ so sorting works
    def __lt__(self, other_card):
        return self.__value < other_card.value

    @property
    def desc(self):
        return self.__desc

    @property
    def value(self):
        return self.__value



