#!/usr/bin/python3

"""
Class that represents player
Keeps track of what/how many cards they have

"""

from card import Card
from hand import Hand
from typing import List, Tuple
import bisect, logging, sys, time

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(message)s")
#logging.disable(logging.DEBUG)

class Player:

    # Attributes
    # hand      - Hand of cards faceup on table
    # name      - the player's name (string)
    
    def __init__(self, name):
        self.__hand = Hand()
        self.__name = name

    # Our getter methods
    @property
    def hand(self):
        return self.__hand

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    # For human players, takes input from stdin
    def guess_range(self) -> int:
        guess = input()

        return guess # Placeholder for now









