#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 23:48:02 2019

@author: slimjimmy
"""

# Casino game involving a deck of cards
# Aim is to get as close as possible to a hand worth 21 points
# Beyond 21 you are out
# Number cards are worth their face value, picture cards are worth 10
# An Ace is either 1 or 11 depending on your other cards
# Players are initially dealt two cards and can either choose to hit (receive 
# another card) or stick (submit their current hand)
# Players face off against the dealer who has one card face down and one face 
# up. When all players have chosen to stick or are out (having over 21), the 
# winner is the one with a hand closest to 21

# Suits: Hearts, Diamonds, Spades and Clubs
# Ranks: Ace, King, Queen, Jack, 1, 2, 3, 4, 5, 6, 7, 8 and 9

import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        
    def __repr__(self): # Changes how the cards are displayed when we call print
        return " of ".join((self.value, self.suit))
    
class Deck:
    def __init__(self):
        self.cards = [Card(s, v) for s in ["Spades", "Clubs", "Hearts", 
                      "Diamonds"] for v in ["A", "2", "3", "4", "5", "6",
                      "7", "8", "9", "10", "J", "Q", "K"]]
        
    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)
    
    def deal(self):
        if len(self.cards) > 1:
            return self.cards.pop(0)
        
class Hand:
    def __init__(self, dealer=False):
        self.dealer = dealer
        self.cards = []
        self.value = 0
        
    def add_card(self, card):
        self.cards.append(card)
        
    def calculate_value(self):
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
        self.calculate_value()
        return self.value
    
    def display(self):
        if self.dealer:
            print ("Hidden")
            print (self.cards[1])
        else:
            for card in self.cards:
                print (card)
            print ("Value:", self.get_value())
            
class Game:
    def __init__(self):
        playing = True
        
        while playing:
            self.deck = Deck()
            self.deck.shuffle()
            
            self.player_hand = Hand()
            self.dealer_hand = Hand(dealer=True)
            
            for i in range(2):
                self.player_hand.add_card(self.deck.deal())
                self.dealer_hand.add_card(self.deck.deal())
                
            print ("Your hand is:")
            self.player_hand.display()
            print ()
            print ("Dealer's hand is:")
            self.dealer_hand.display()
            
            game_over = False
        
            while not game_over:
                player_has_blackjack, dealer_has_blackjack = self.check_for_blackjack()
                if player_has_blackjack or dealer_has_blackjack:
                    game_over = True
                    self.show_blackjack_results(player_has_blackjack, dealer_has_blackjack)
                    continue
                choice = input("Please choose [Hit / Stick]: ").lower()
                while choice not in ["h", "s", "hit", "stick"]:
                    choice = input("Please enter 'hit' or 'stick' (or H/S) ").lower()
                if choice in ['hit', 'h']:
                    self.player_hand.add_card(self.deck.deal())
                    self.player_hand.display()
                if self.player_is_over():
                    print ("You have lost!")
                    game_over = True
                else:
                    print ("Final Results")
                    print ("Your hand:", self.player_hand.get_value())
                    print ("Dealer's hand:", self.dealer_hand.get_value())
                    
                    if self.player_hand.get_value() > self.dealer_hand.get_value():
                        print ("You win!")
                        game_over = True
                    else:
                        print ("Dealer wins!")
                        game_over = True
            again = input("Play Again? [Y/N] ")
            while again.lower() not in ["y", "n"]:
                again = input("Please enter Y or N ")
            if again.lower() == "n":
                print("Thanks for playing!")
                playing = False
            
    def check_for_blackjack(self):
        player = False
        dealer = False
        if self.player_hand.get_value() == 21:
            player = True
        if self.dealer_hand.get_value() == 21:
            dealer = True
            
        return player, dealer
    
    def show_blackjack_results(self, player_has_blackjack, dealer_has_blackjack):
        if player_has_blackjack and dealer_has_blackjack:
            print ("Both players have blackjack! Draw!")
            
        elif player_has_blackjack:
            print ("You have blackjack! You win!")
            
        elif dealer_has_blackjack:
            print ("Dealer has blackjack! Dealer wins!")
            
    def player_is_over(self):
        return self.player_hand.get_value() > 21
            
if __name__ == "__main__":
    game = Game()