#!/usr/bin/python3

"""
Class for representing cards in the game

"""

class Card:

    # Attributes
    # desc  - A description of the unfortunate scenario on said card
    # value - The misery index value assigned to this card (float)

    def __init__(self, desc, value):
        self.desc  = desc
        self.value = value

    def getDesc(self):
        return self.desc

    def getValue(self):
        return self.value


