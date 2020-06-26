#!/usr/bin/python3

"""
Represents the board of the game
Keeps track of the current game state
"""

# Project file imports
from player import Player
from card import Card
from card_list import card_list
from exceptions import NoCardError, NumPlayerError, TimeoutExpiredError

# Library imports
import random, re
import logging
import pprint
import sys
import traceback
import select

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
# logging.disable(logging.DEBUG)

class Board:

    STARTING_CARDS = 3
    MAX_PLAYERS = 8

    # Game end conditions:
        # Player obtains 10 cards
        # Deck runs out of cards

    # TODO: (Stretch)
        # - Database to handle cards   
        # - GUI in browser
        # - Timed input for non-stdin
        # - Network programming for multiplayer

    # Attributes:
        # current_guesser  - The current Player guessing
        # current_leader   - Current player in the lead - tentative
        # current_starter  - The first player guessing for a particular round
        # deck             - A list of Cards
        # discard_pile     - List of discarded cards that no one guessed
        # num_players      - The number of Players
        # players          - A list of Players, all the people playing the game
        # previous_guesses - List of tuples containing range guesses of other players for current round

    # Initialiser/constructor
    def __init__(self, players):

        # Create the game deck + discard pile here
        self.discard_pile = list()
        self.deck = self.initialise_deck()
        random.shuffle(self.deck)
        self.num_cards = len(self.deck)

        # Players get passed in to class    
        self.players         = list() 
        self.current_guesser = None
        self.current_starter = None

        # Unlike other two "current" values, this will just be reference to player (since order doesn't matter)
        # Current leader is always one person, the first person to the highest score
        self.current_leader  = None
        
        try:
            self.initialise_players(players)

        # Game needs at least 2 players to start
        # Number of players also can't exceed MAX_PLAYERS
        except NumPlayerError as e:
            print(e)
            self.end_game()

        # There also needs to be enough cards for each player to have a starting hand
        except NoCardError:
            print("Not enough cards in the deck to be able to play the game")
            self.end_game()
            
        # Shows everyone's starting cards 
        self.print_player_cards()

        self.previous_guesses = list()

    # Draws a card from the deck
    def draw_card(self):
        try:
            nextCard = self.deck.pop()
            self.num_cards -= 1
        except IndexError:
            raise NoCardError("No more cards left in deck!")

        return nextCard

    # This is the mumma function which will handle each turn
    # Draw card -> first player guess -> ... -> until correct guess or everyone incorrectly guesses
    def game_turns(self):
        
        # Sanity check to see if we have enough cards in the deck before starting first draw
        try:
            new_card = self.draw_card()

        except NoCardError:
            print("Game over - no one wins because there's not enough cards to start the game")
            self.end_game()

        self.print_next_turn_text()

        # While there's still cards in the deck and victory condition hasn't been reached
        while new_card:
            guess_player = self.players[self.current_guesser]
            print(f"{guess_player.name}'s turn to guess")
            print(''.rjust(20, '>'))
            print()

            # If guess is correct, update new leader if necessary and check victory conditions before drawing card
            if self.handle_guess(new_card):
                if self.current_leader is None or \
                    guess_player.hand.num_cards > self.current_leader.hand.num_cards:
                        self.current_leader = self.players[self.current_guesser]

                # Check victory conditions
                new_card = self.game_over_check(guess_player)

            # next_guesser returns None if everyone already attempted a guess for this round 
            elif not self.next_guesser():
                print(f"Everyone failed the guess. The correct value was {new_card.value}") 
                self.discard_pile.append(new_card)

                # Check victory conditions
                new_card = self.game_over_check(guess_player)
       
        print("Game over!")
        
        if self.current_leader is None:
            print("No one wins!")

        else:
            print(f"{self.current_leader.name} wins!")

        print("See ya later!")
        self.end_game()

    # Handle's a given player's guess. Returns True if correct, False if not
    def handle_guess(self, new_card):
        player = self.players[self.current_guesser]

        print(f"Card description: {new_card.desc}")

        if self.previous_guesses:
            print("Ranges guessed incorrectly by previous players:")
            for g in self.previous_guesses:
                print(g, end=' ')

            print()

        print()
        print("Where in the range of your card's values do you think this card lies?")
        print("Choose a number from the following:")


        for i, val in enumerate(player.hand.ranges):
            print(f"{i + 1}.) Between {val[0]} and {val[1]}")

        #TODO: In future version, implement timeout via multithreading when not reading stdin
        #      Have to do it this way for now since input blocks everything else
        try:
            guessIndex = int(player.guess_range()) - 1

        # Check if Integer was given
        except ValueError:
            print("Error - Invalid input, counts as wrong guess")
            return False 

        # Check if the guess timer expired
        except TimeoutExpiredError:
            print("Error - input timed out, counts as wrong guess")
            return False

        # Make sure given option is valid 
        if guessIndex < 0 or guessIndex > player.hand.num_cards: 
            print("Invalid option given, counts as wrong guess")
            return False

        # Check guessed range, return True if card misery index lies in that range
        guessedRange = player.hand.ranges[guessIndex]
        if guessedRange[0] <= new_card.value <= guessedRange[1]: 
            print("Your guess was correct! You gained a new card =D")
            player.hand.gain_card(new_card)
            return True
        
        # Add guessed range to previous guesses if wrong
        else:
            print("Unfortunately your guess was incorrect =(")
            self.previous_guesses.append(guessedRange)

        return False

    # Returns None when everyone has had a turn guessing
    def next_guesser(self):
        self.current_guesser += 1
        self.current_guesser = self.current_guesser % self.num_players

        if self.current_guesser == self.current_starter:
            return
        
        return self.players[self.current_guesser]
    
    def next_turn(self):
        self.current_starter += 1
        self.current_starter = self.current_starter % self.num_players
        self.current_guesser = self.current_starter
        self.previous_guesses = []

        self.print_next_turn_text()

    def start_game(self):
        self.game_turns()

    # Initialisation Functions
    ###################################################

    # Creates list of cards
    # Current implementation: Import card list and make card objects for each 
    def initialise_deck(self):
        deck = list()

        for desc, index in card_list:
            new_card = Card(desc, index)
            deck.append(new_card)

        return deck

    def initialise_players(self, players):
        names = dict()
        length = len(players)
        i = 0

        while i < length:
            next_name = players[i].name

            # If player doesn't have name, call them Gary
            if not next_name:
                next_name = "Gary"

            # If player has same name, put a number on the end of their name in brackets
            # Basically the same way XBL handles duplicate names
            if next_name in names:
                a = names[next_name]
                while (next_name + f"({a})") in names:
                   a += 1
                next_name += f"({a})"

                names[players[i].name] = a

            # Once name is valid, put player in player list
            players[i].name = next_name
            self.players.append(players[i])
           
            # Increment index, mark name as taken so another player can't have it
            i += 1
            names[next_name] = 1

        self.num_players = len(self.players)

        # Cases for NumPlayerError - Either having less than 2 players or more than max players
        if self.num_players < 2:
            raise NumPlayerError("Error - Must have at least two players")

        if self.num_players > self.MAX_PLAYERS:
            raise NumPlayerError(f"Error - Can't have more than {self.MAX_PLAYERS} players.")

        # Give players their starting cards
        self.initialise_player_cards()    

        # Shuffle players to have a random starter
        random.shuffle(self.players) #TODO: turn on again after testing
        self.current_starter = 0

        # First guesser is the first starter
        self.current_guesser = 0

    # Initialises player hands - each player starts with 3 cards
    def initialise_player_cards(self):
        for player in self.players:
            for _ in range(self.STARTING_CARDS):
                player.hand.gain_card(self.draw_card())
    
    ###################################################


    # Returns None if game over, otherwise returns the next card for the game
    def game_over_check(self, guess_player=None):
        # Game Over Condition 1: If player reaches 10 cards
        if guess_player is not None and \
            guess_player.hand.num_cards == 10:
                print(f"{guess_player.name} has 10 cards...")
                return None

        # Game Over Condition 2: If deck runs out of cards 
        if self.num_cards == 0:
            print("There are no more cards left in the deck...")
            return None
        
        self.next_turn()

        return self.draw_card() 

    def end_game(self):
        # Not sure how this will work later, functionalised it to make it easier
        sys.exit()


    # Printing functions 
    ###################################################

    # prints info for next turn
    def print_next_turn_text(self):
        print(''.rjust(30,'-'))
        print(f"{self.players[self.current_starter].name} will start the round...")
        print(''.rjust(30,'-'))
        print()

    # Currently used for showing player hands during each round/guess
    # Will be changed in future versions no doubt
    def print_player_cards(self):
        for player in self.players:
            print(f"Player {player.name}'s cards: ({player.hand.num_cards} total)")
            player.hand.print_hand() 

    # Property decorators/misc debug funcs - i.e. for testing/playing around with how they work
    ###################################################

    # def print_deck(self):
        # out = ''
        # out += "["
        # for card in self.deck:
            # out += f"""("{card.desc}", {card.value}),\n"""

        # out += "]"
        # print(out, file=open("card_list.py", "w"))

    # @property
    # def deck(self):
        # return self.__deck

    # @property
    # def current_guesser(self):
        # return self.__current_guesser

    # @property
    # def current_starter(self):
        # return self.__current_starter

