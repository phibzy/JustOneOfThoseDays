#!/usr/bin/python3

"""
Represents the board of the game
Keeps track of the current game state
"""

from player import Player
from card import Card
from typing import List, Tuple
import random, re
import logging
import pprint
import sys

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
# logging.disable(logging.DEBUG)

class Board:

    STARTING_CARDS = 3

    # Game end conditions:
    # Player obtains 10 cards
    # Deck runs out of cards

    # Game currently assumes that there will be no equal valued cards
        # Or that if there are equal valued cards, you can end up with ranges like (5,7), (7,7), (7,10)

    # TODO: A GAME STATE:
        # - Hash with player names as key
            # - Make sure player names unique - add 1 to their names if not unique
            # - num_cards for each player
            # - list of cards for each player
            # - list of ranges for each player

        # - previous_guesses: list of guessed ranges. Reset at beginning of every turn
        # - Current leader (maybe)

    # TODO:
        # - Handle individual guesses (player.guess_range, define board method for guess handling)
        # - Handle each round
        # - Handling previous guesses properly

    # Attributes
    # current_guesser  - The current Player guessing
    # current_leader   - Current player in the lead - tentative
    # current_starter  - The first player guessing for a particular round
    # deck             - A list of Cards
    # discard_pile     - List of discarded cards that no one guessed
    # num_players      - The number of Players
    # players          - A list of Players, all the people playing the game
    # previous_guesses - List of tuples containing range guesses of other players for current round
        #Note: To handle end ranges, do (0,x) and (x, 101)

    # May want dict keeping track of scores, as the board object is
    # what will ultimately signal end of game

    # Initialiser/constructor
    def __init__(self, players):

        # Create the game deck + discard pile here
        self.__discard_pile = list()
        self.__deck = self.__initialise_deck()
        random.shuffle(self.__deck)
        self.__num_cards = len(self.__deck)

        # Players get passed in to class    
        self.__players         = list() 
        self.__current_guesser = None
        self.__current_starter = None
        self.__current_leader  = None
        
        try:
            self.__initialise_players(players)
        except:
            print("Error - Not enough players. Minimum 2 required")

        self.__print_player_cards()

        self.__previous_guesses = list()


    # This is the mumma function which will handle each turn
    # Draw card -> first player guess -> ... -> until correct guess or back to first player again
    def game_turns(self):
        
        try:
            newCard = self.draw_card()
        except:
            print("Game over - no one wins because there's not enough cards to start the game")
            sys.exit()

        while newCard:

            if self.handle_guess(newCard):
                if self.__num_cards == 0:
                    break
                    #TODO: Update current_leader
                    #TODO: Game over if player reaches 10 cards

                self.next_turn()

            elif not self.next_guesser():
                self.__discard_pile.append(newCard)
                try:
                    newCard = self.draw_card()
                except:
                    print("No more cards in deck!")
                    break

       
        #TODO: Current leader is the winner!
        print("Game over! See ya later!")


    def handle_guess(self, newCard):
        player = self.__current_guesser

        print(f"Card description: {newCard.desc}")
        print("Where in the range of your card's values do you think this card lies?")
        print("Choose a number from the following:")

        for i, val in enumerate(player.hand.ranges):
            print(f"{i + 1}.) Between {val[0]} and {val[1]}")

        guessIndex = player.guess_range(newCard.desc) - 1

        #TODO: input checking (i.e. make sure it's an int)
        if guessIndex < 0 or guessIndex > player.num_cards: 
            print("Invalid option given, counts as wrong guess")
            return False

        guessedRange = player.ranges[guessIndex]
        if guessedRange[0] <= newCard.value <= guessedRange[1]: 
            print("Your guess was correct! You gained a new card =D")
            player.hand.gain_card(newCard)
            return True

        return False

    def draw_card(self):
        try:
            nextCard = self.__deck.pop()
            self.__num_cards -= 1
        except IndexError:
            raise Exception("No more cards left in deck!")

        return nextCard

    # For debugging purposes - will remove later
    ###################################################

    @property
    def deck(self):
        return self.__deck

    @property
    def current_guesser(self):
        return self.__current_guesser

    @property
    def current_starter(self):
        return self.__current_starter

    ###################################################


    def __initialise_deck(self):
        cardRegex = re.compile(r"^(.*) (.*\d)$")
        deck = list()

        f1 = open("card_list.txt")
        for line in f1.readlines():
            mo = cardRegex.search(line)
            newCard = Card(mo.group(1), float(mo.group(2))) 
            deck.append(newCard)

        f1.close()
       
        return deck

    def __initialise_players(self, players):
        names = dict()
        playerList = list()

        i = 0
        length = len(players)

        while i < length:
            nextName = players[i]
            a = 1
            while nextName in names:
               nextName += a
               a += 1
            i += 1

            names[nextName] = True
            self.__players.append(nextName)

        self.__num_players = len(self.__players)
        
        if self.__num_players < 2:
            raise Exception("Must have at least two players")

        # Give players their starting cards
        try:
            self.__initialise_player_cards()    
        except:
            raise Exception("Not enough cards in deck")

        # Shuffle players to have a random starter
        random.shuffle(self.__players)
        self.__current_starter = self.__players[0]

        # First guesser is the first starter
        self.__current_guesser = self.__current_starter

    def __initialise_player_cards(self):
        # Each player draws 3 cards
        for player in self.__players:
            for _ in range(self.STARTING_CARDS):
                player.hand.gain_card(self.draw_card())
   
    # Returns None when everyone has had a turn guessing
    def next_guesser(self):
        self.__current_guesser += 1
        self.__current_guesser = self.__current_guesser % self.__num_players

        if self.__current_guesser == self.current_starter:
            return
        
        return self.__players[self.__current_guesser]

    def next_turn(self):
        self.__current_starter += 1
        self.__current_starter = self.__current_starter % self.__num_players
        self.__current_guesser = self.__current_starter
        self.__previous_guesses = []

        return self.__players[self.__current_starter]

    ##### DEBUG METHODS ######
    def print_player_cards(self):
        for player in self.__players:
            print(f"Player {player.name}'s cards: ({player.num_cards} total)")
            player.hand.print_hand() 


