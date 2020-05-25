#!/usr/bin/python3

"""
Represents the board of the game
Keeps track of the current game state
"""

# Project file imports
from player import Player
from card import Card
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

    # TODO:
        # - Implement timeout for player range guesses
        # - At least 100 cards 
        # - Network programming for multiplayer

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

        # Unlike other two "current" values, this will just be reference to player (since order doesn't matter)
        # Current leader is always one person, the first person to the highest score
        self.__current_leader  = None
        
        try:
            self.__initialise_players(players)

        # Game needs at least 2 players to start
        # Number of players also can't exceed MAX_PLAYERS
        except NumPlayerError as e:
            print(e)
            self.end_game()

        # There also needs to be enough cards for each player to have a starting hand
        except NoCardError:
            print("Not enough cards in the deck to be able to play the game")
            self.end_game()
            
        self.print_player_cards()

        self.__previous_guesses = list()

        # Run the actual game
        self.game_turns()


    # This is the mumma function which will handle each turn
    # Draw card -> first player guess -> ... -> until correct guess or back to first player again
    def game_turns(self):
        
        try:
            new_card = self.draw_card()
        except NoCardError:
            print("Game over - no one wins because there's not enough cards to start the game")
            self.end_game()

        self.print_next_turn_text()

        while new_card:
            guess_player = self.__players[self.__current_guesser]
            print(f"{guess_player.name}'s turn to guess")
            print(''.rjust(20, '>'))
            print()

            if self.handle_guess(new_card):
                if self.__current_leader is None or \
                    guess_player.hand.num_cards > self.__current_leader.hand.num_cards:
                        self.__current_leader = self.__players[self.__current_guesser]

                # Check victory conditions
                new_card = self.game_over_check(guess_player)

            elif not self.next_guesser():
                print(f"Everyone failed the guess. The correct value was {new_card.value}") 
                self.__discard_pile.append(new_card)

                # Check victory conditions
                new_card = self.game_over_check(guess_player)
       
        print("Game over!")
        
        if self.__current_leader is None:
            print("No one wins!")

        else:
            print(f"{self.__current_leader.name} wins!")

        print("See ya later!")
        self.end_game()


    def handle_guess(self, new_card):
        player = self.__players[self.__current_guesser]

        print(f"Card description: {new_card.desc}")

        if self.__previous_guesses:
            print("Ranges guessed incorrectly by previous players:")
            for g in self.__previous_guesses:
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
        except ValueError:
            print("Error - Invalid input, counts as wrong guess")
            return False 
        except TimeoutExpiredError:
            print("Error - input timed out, counts as wrong guess")
            return False

        if guessIndex < 0 or guessIndex > player.hand.num_cards: 
            print("Invalid option given, counts as wrong guess")
            return False

        guessedRange = player.hand.ranges[guessIndex]
        if guessedRange[0] <= new_card.value <= guessedRange[1]: 
            print("Your guess was correct! You gained a new card =D")
            player.hand.gain_card(new_card)
            return True
        
        # Add guessed range to previous guesses if wrong
        else:
            print("Unfortunately your guess was incorrect =(")
            self.__previous_guesses.append(guessedRange)

        return False

    def draw_card(self):
        try:
            nextCard = self.__deck.pop()
            self.__num_cards -= 1
        except IndexError:
            raise NoCardError("No more cards left in deck!")

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


    # Initialisation Functions
    ###################################################

    def __initialise_deck(self):
        cardRegex = re.compile(r"^(.*) (.*\d)$")
        deck = list()

        f1 = open("card_list.txt")
        for line in f1.readlines():
            mo = cardRegex.search(line)
            new_card = Card(mo.group(1), float(mo.group(2))) 
            deck.append(new_card)

        f1.close()
       
        return deck

    def __initialise_players(self, players):
        names = dict()
        length = len(players)
        i = 0

        while i < length:
            nextName = players[i].name

            # If player doesn't have name, call them Gary
            if not nextName:
                nextName = "Gary"

            # If player has same name, put a number on the end of their name
            if nextName in names:
                a = 2
                while (nextName + str(a)) in names:
                   a += 1
                nextName += str(a)

            players[i].name = nextName
            self.__players.append(players[i])
            
            i += 1
            names[nextName] = True

        self.__num_players = len(self.__players)

        if self.__num_players < 2:
            raise NumPlayerError("Error - Must have at least two players")

        if self.__num_players > self.MAX_PLAYERS:
            raise NumPlayerError(f"Error - Can't have more than {self.MAX_PLAYERS} players.")

        # Give players their starting cards
        self.__initialise_player_cards()    

        # Shuffle players to have a random starter
        random.shuffle(self.__players)
        self.__current_starter = 0

        # First guesser is the first starter
        self.__current_guesser = 0

    def __initialise_player_cards(self):
        # Each player draws 3 cards
        for player in self.__players:
            for _ in range(self.STARTING_CARDS):
                player.hand.gain_card(self.draw_card())
    
    ###################################################


   
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

        self.print_next_turn_text()

    def print_next_turn_text(self):
        print(''.rjust(30,'-'))
        print(f"{self.__players[self.__current_starter].name} will start the round...")
        print(''.rjust(30,'-'))
        print()

    # Returns None if game over, otherwise returns the next card for the game
    def game_over_check(self, guess_player=None):
        # Game Over Condition 1: If player reaches 10 cards
        if guess_player is not None and \
            guess_player.hand.num_cards == 10:
                print(f"{guess_player.name} has 10 cards...")
                return None

        # Game Over Condition 2: If deck runs out of cards 
        if self.__num_cards == 0:
            print("There are no more cards left in the deck...")
            return None
        
        self.next_turn()

        return self.draw_card() 

    def end_game(self):
        # Not sure how this will work later, functionalised it to make it easier
        sys.exit()

    ##### DEBUG METHODS ######
    def print_player_cards(self):
        for player in self.__players:
            print(f"Player {player.name}'s cards: ({player.hand.num_cards} total)")
            player.hand.print_hand() 


