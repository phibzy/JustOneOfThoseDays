#!/usr/bin/python3

"""
Class that represents player
Keeps track of what/how many cards they have

"""

class Player:

    # Attributes
    # cards     - a list of current Cards faceup on table
    # name      - the player's name
    # numCards  - an int with number of cards player has
    
    def __init__(self, name, cards):
        self.cards = cards
        self.name = name
        self.numCards = 1 # Each player starts with one card
                          # Possibly change this to 0 depending on how first card is handled

    # Our getter methods
    def getCards(self):
        pass

    def getName(self):
        return self.name

    def getNumCards(self):
        return self.numCards

    # Adds card to Player's faceup cards if they guess correctly
    def gainCard(self, newCard):
        self.cards.append(newCard) # Want to insert it in order
        self.numCards += 1

    # Method for checking where card lies in range of Player's cards
    def checkCard(self, newCard):
        pass
