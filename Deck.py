import random

# Face values of cards
FACES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
# Initial value of cards in order of faces; based on blackjack card values
VALUES = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
# Suit values of cards
SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
SUIT_IMAGES = '♥♦♣♠'


class Card:
    """Card object for card games"""
    def __init__(self, face, suit, value=0, face_down=False):
        """

        :param face: Face value of playing card
        :type face: str
        :param suit: Suit value of playing card
        :type suit: str
        :param value: Point value of playing card
        :type value: int
        :param face_down: Visibility of playing card
        :type face_down: bool
        """
        self.face = face
        self.suit = suit
        self.value = value
        self.face_down = face_down

    def __str__(self) -> str:
        """

        :return: String representation of Card object
        :rtype: str
        """
        return f"{self.face}-{self.suit}"

    def flip(self):
        """Flip value of face_down boolean"""
        self.face_down = False if self.face_down else True


class Deck:
    """Deck object for card games"""
    def __init__(self, num_of_decks=1, shuffled=False):
        """

        :param num_of_decks: Number of 52 card decks
        :type num_of_decks: int
        :param shuffled: Organization of Cards
        :type shuffled: bool
        """
        self.num_of_decks = num_of_decks
        
        # populate Deck with Card objects
        self.cards = [Card(f, s, v)
                      for f, v in zip(FACES * num_of_decks, VALUES * num_of_decks)
                      for s in SUIT_IMAGES]

        # shuffle Deck
        if shuffled:
            random.shuffle(self.cards)

    def __len__(self) -> int:
        """

        :return: Number of cards in Deck object
        :rtype: int
        """
        return len(self.cards)

    def deal_card(self) -> object:
        """

        :return: Last card in Deck
        :rtype: Card
        """
        if len(self.cards) > 0:
            return self.cards.pop()
