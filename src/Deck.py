import random
from src.Card import Card


class EmptyDeck(Exception):
    pass


class Deck:
    """A class representing a deck of cards"""

    FACES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    VALUES = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
    SUIT_IMAGES = "♥♦♣♠"

    def __init__(self, num_of_decks=1, shuffled=False):
        self.num_of_decks = num_of_decks
        self.cards = [
            Card(f, s, v)
            for f, v in zip(Deck.FACES * num_of_decks, Deck.VALUES * num_of_decks)
            for s in Deck.SUIT_IMAGES
        ]

        if shuffled:
            random.shuffle(self.cards)

    def __len__(self) -> int:
        return len(self.cards)

    def deal_card(self) -> Card:
        if not self.cards:
            raise EmptyDeck
        return self.cards.pop()
