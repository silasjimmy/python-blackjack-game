#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 14:57:15 2020

@author: slimjimmy
"""

import tkinter as tk
import os # to access the images folder
import random # to shuffle the deck

assets_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets/'))

class Card:
    def __init__(self, suit, value):
        '''
        suit: Card's suit
        value: Card's rank
        '''
        self.suit = suit
        self.value = value
        self.img = tk.PhotoImage(file=assets_folder + '/' + self.suit + self.value + ".png")

    def __repr__(self):
        '''
        Returns the string representation of the card
        '''
        return " of ".join((self.value, self.suit))

    def get_file(self):
        '''
        Returns the card image
        '''
        return self.img

    @classmethod
    def get_back_file(cls):
        '''
        Returns the back image of a card representing a card face down
        '''
        cls.back = tk.PhotoImage(file=assets_folder + "/back.png")

        return cls.back
    
class Deck:
    def __init__(self):
        self.cards = [Card(s, v) for s in ["Spades", "Clubs", "Hearts", "Diamonds"] for v in
                      ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]]

    def shuffle(self):
        '''
        Shuffles the deck of cards
        '''
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self):
        '''
        Returns a single card from the top of the deck
        '''
        if len(self.cards) > 1:
            return self.cards.pop(0)
        
class Hand:
    def __init__(self, dealer=False):
        '''
        dealer: Specifies if the hand created ifs for the dealer
        '''
        self.dealer = dealer
        self.cards = []
        self.value = 0

    def add_card(self, card):
        '''
        Adds a card to the hand
        '''
        self.cards.append(card)

    def calculate_value(self):
        '''
        Calculates the value of the cards in a hand
        '''
        self.value = 0
        has_ace = False
        for card in self.cards:
            if card.value.isnumeric():
                self.value += int(card.value)
            else:
                if card.value == "A":
                    has_ace = True
                    self.value += 11
                else:
                    self.value += 10

        if has_ace and self.value > 21:
            self.value -= 10

    def get_value(self):
        '''
        Returns the value of the hand
        '''
        self.calculate_value()
        return self.value
    
class GameState:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()

        self.player_hand = Hand() # Create a player's hand
        self.dealer_hand = Hand(dealer=True) # Create a dealer's hand

        for i in range(2): # Deal the dealer and the player two cards each
            self.player_hand.add_card(self.deck.deal())
            self.dealer_hand.add_card(self.deck.deal())

        self.has_winner = '' # Initialize the winner as nobody

    def hit(self):
        '''
        Adds a card to the player's hand if he decides to hit
        '''
        self.player_hand.add_card(self.deck.deal())
        if self.someone_has_blackjack() == 'p':
            self.has_winner = 'p' # The player wins if he has blackjack
        if self.player_is_over():
            self.has_winner = 'd' # The dealer wins if the player's hand is over 21

        return self.has_winner

    def get_table_state(self):
        '''
        Returns information of the table's state between each hit
        '''
        blackjack = False
        winner = self.has_winner
        if not winner:
            winner = self.someone_has_blackjack() # Update the winner variable
            if winner:
                blackjack = True
        table_state = {
            'player_cards': self.player_hand.cards,
            'dealer_cards': self.dealer_hand.cards,
            'has_winner': winner,
            'blackjack': blackjack,
        }

        return table_state

    def calculate_final_state(self):
        '''
        Called when the player decides to stick with their hand.
        This signals the final state of the hand
        '''
        player_hand_value = self.player_hand.get_value()
        dealer_hand_value = self.dealer_hand.get_value()

        if player_hand_value == dealer_hand_value:
            winner = 'dp'
        elif player_hand_value > dealer_hand_value:
            winner = 'p'
        else:
            winner = 'd'

        table_state = {
            'player_cards': self.player_hand.cards,
            'dealer_cards': self.dealer_hand.cards,
            'has_winner': winner,
        }

        return table_state

    def player_score_as_text(self):
        '''
        Returns the player's score as text
        '''
        return "Score: " + str(self.player_hand.get_value())

    def someone_has_blackjack(self):
        '''
        Signals which contenstant (if any) is the one with blackjack.
        Blackjack is when a player's hand totals to a value of 21
        '''
        player = False
        dealer = False
        if self.player_hand.get_value() == 21:
            player = True
        if self.dealer_hand.get_value() == 21:
            dealer = True

        if player and dealer:
            return 'dp' # If both the dealer and player have blackjack
        elif player:
            return 'p' # If the player has blackjack
        elif dealer:
            return 'd' # If the dealer has blackjack

        return False # If nobody has blackjack

    def player_is_over(self):
        return self.player_hand.get_value() > 21
    
class GameScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Blackjack")
        self.geometry("800x640")
        self.resizable(False, False)

        self.CARD_ORIGINAL_POSITION = 100 # X coordinate at which the first card dealt to the player and dealer is placed
        self.CARD_WIDTH_OFFSET = 100 # Space between each playing card in the X direction

        self.PLAYER_CARD_HEIGHT = 300 # Y coordinate where the player's card will be displayed
        self.DEALER_CARD_HEIGHT = 100 # Y coordinate where the dealer's card will be displayed

        self.PLAYER_SCORE_TEXT_COORDS = (400, 450) # Coordinates where the score will be displayed
        self.WINNER_TEXT_COORDS = (400, 250) # Coordinates where the text indicating the winner will be displayed

        self.game_state = GameState()

        self.game_screen = tk.Canvas(self, bg="white", width=800, height=500) # Create a fresh copy of the screen whenever we begin a new game

        self.bottom_frame = tk.Frame(self, width=800, height=140, bg="red") # Bottom frame where the buttons are placed
        self.bottom_frame.pack_propagate(0)

        self.hit_button = tk.Button(self.bottom_frame, text="Hit", width=25, command=self.hit)
        self.stick_button = tk.Button(self.bottom_frame, text="Stick", width=25, command=self.stick)

        self.play_again_button = tk.Button(self.bottom_frame, text="Play Again", width=25, command=self.play_again)
        self.quit_button = tk.Button(self.bottom_frame, text="Quit", width=25, command=self.destroy)

        self.hit_button.pack(side=tk.LEFT, padx=(100, 200))
        self.stick_button.pack(side=tk.LEFT)

        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.game_screen.pack(side=tk.LEFT, anchor=tk.N)

        self.display_table()

    def display_table(self, hide_dealer=True, table_state=None):
        '''
        hide_dealer: True to hide the dealer's first card, False otherwise
        Draws the graphical elements to the canvas
        '''
        if not table_state: # Generate a table state if not provided in the argument table_state
            table_state = self.game_state.get_table_state()

        player_card_images = [card.get_file() for card in table_state['player_cards']]
        dealer_card_images = [card.get_file() for card in table_state['dealer_cards']]
        if hide_dealer and not table_state['blackjack']:
            dealer_card_images[0] = Card.get_back_file() # Show the back image of a card if the hide_dealer and table_state both are true

        self.game_screen.delete("all") # Delete everything currently drawn to the canvas between each draw
        self.tabletop_image = tk.PhotoImage(file=assets_folder + "/tabletop.png") # Image used as the background of the canvas

        self.game_screen.create_image((400, 250), image=self.tabletop_image)

        for card_number, card_image in enumerate(player_card_images):
            self.game_screen.create_image(
                (self.CARD_ORIGINAL_POSITION + self.CARD_WIDTH_OFFSET * card_number, self.PLAYER_CARD_HEIGHT),
                image=card_image
            )

        for card_number, card_image in enumerate(dealer_card_images):
            self.game_screen.create_image(
                (self.CARD_ORIGINAL_POSITION + self.CARD_WIDTH_OFFSET * card_number, self.DEALER_CARD_HEIGHT),
                image=card_image
           )

        self.game_screen.create_text(self.PLAYER_SCORE_TEXT_COORDS, text=self.game_state.player_score_as_text(), font=(None, 20))

        if table_state['has_winner']:
            if table_state['has_winner'] == 'p':
                self.game_screen.create_text(self.WINNER_TEXT_COORDS, text="YOU WIN!", font=(None, 50))
            elif table_state['has_winner'] == 'dp':
                self.game_screen.create_text(self.WINNER_TEXT_COORDS, text="TIE!", font=(None, 50))
            else:
                self.game_screen.create_text(self.WINNER_TEXT_COORDS, text="DEALER WINS!", font=(None, 50))

            self.show_play_again_options()

    def show_play_again_options(self):
        '''
        Unpacks the hit and stick button then packs the 
        play again and hit buttons
        '''
        self.hit_button.pack_forget()
        self.stick_button.pack_forget()

        self.play_again_button.pack(side=tk.LEFT, padx=(100, 200))
        self.quit_button.pack(side=tk.LEFT)

    def show_gameplay_buttons(self):
        '''
        Unpacks the play again and hit buttons then packs the 
        hit and stick buttons
        '''
        self.play_again_button.pack_forget()
        self.quit_button.pack_forget()

        self.hit_button.pack(side=tk.LEFT, padx=(100, 200))
        self.stick_button.pack(side=tk.LEFT)

    def play_again(self):
        '''
        Initializes a new game
        '''
        self.show_gameplay_buttons()
        self.game_state = GameState()
        self.display_table()

    def hit(self):
        '''
        Call hit method of the game state then update the table
        by drawing it again
        '''
        self.game_state.hit()
        self.display_table()

    def stick(self):
        '''
        Ends any further game logic
        '''
        table_state = self.game_state.calculate_final_state()
        self.display_table(False, table_state)
        
if __name__ == "__main__":
    game_screen = GameScreen()
    game_screen.mainloop()