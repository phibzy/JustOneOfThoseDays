#!/usr/bin/python3

"""
Class that represents player
Keeps track of what/how many cards they have

"""

from card import Card
from hand import Hand
from exceptions import TimeoutExpiredError

import bisect, logging, select, sys, time


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
    def guess_range(self):

        # Stdin with timeout of 10 seconds
        guess = input_with_timeout('', 10)

        return guess # Placeholder for now

# courtesy of Stack Overflow user jfs
def input_with_timeout(prompt, timeout):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [],[], timeout)
    if ready:
        return sys.stdin.readline().rstrip('\n') # expect stdin to be line-buffered
    raise TimeoutExpiredError


