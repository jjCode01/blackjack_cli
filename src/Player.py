from src.Deck import Card


class Hand:
    def __init__(self, bet):
        self.cards = []
        self.bet = bet
        self.bet_multiplier = 1.0

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        hand_str = ""
        if len(self) == 0:
            hand_str += "Hand Empty"
        else:

            def card_top(crd):
                return (
                    "|   -   | "
                    if crd.face_down
                    else f"| {crd.face}{' ' * (6 - len(crd.face))}|"
                )

            def card_middle(crd):
                return "|  ---  | " if crd.face_down else f"|   {crd.suit}   |"

            def card_bottom(crd):
                return (
                    "|   -   | "
                    if crd.face_down
                    else f"|{' ' * (6 - len(crd.face))}{crd.face} |"
                )

            hand_str += (
                "┌───────┐" * len(self)
                + "\n"
                + "".join([card_top(c) for c in self.cards])
                + "\n"
                + "|       |" * len(self)
                + "\n"
                + "".join([card_middle(c) for c in self.cards])
                + "\n"
                + "|       |" * len(self)
                + "\n"
                + "".join([card_bottom(c) for c in self.cards])
                + "\n"
                + "└───────┘" * len(self)
                + "\n"
            )

        return hand_str

    @property  # return hand score
    def score(self):
        _score = sum([c.value for c in self.cards if not c.face_down])
        if _score > 21:
            for crd in reversed(self.cards):
                if crd.value == 11:
                    crd.value = 1
                    _score = self.score
                    break

        return _score


class Player:
    """Player object for card games."""

    def __init__(self, player_name: str, money: float, bet: float):
        self.name = player_name
        self.money = money
        self._hand: list[Hand] = [Hand(bet)]
        self._current_hand = 0
        self._num_of_hands = 0

    def __len__(self) -> int:
        return len(self._hand)  # returns the number of hands the player has

    def __str__(self) -> str:
        return (
            f"{self.name}{' Hand ' + str(self.current_hand + 1) if len(self._hand) > 1 else ''}: "
            f"{self.hand.score}\n{'-' * 60}\n{self.hand}"
        )

    @property
    def hand(self) -> Hand:
        return self._hand[self._current_hand]

    @hand.setter  # set player hand
    def hand(self, hand_obj: Hand):
        self._hand = [hand_obj]
        self._current_hand = 0
        self._num_of_hands = 0

    @property
    def hands(self) -> list:
        return self._hand

    @property
    def all_bets(self) -> float:
        return sum([h.bet for h in self._hand])

    @property
    def min_score(self) -> int:
        return min([h.score for h in self._hand])

    @property
    def bank(self) -> float:
        return self.money - self.all_bets

    @property
    def score(self) -> int:
        return self._hand[self._current_hand].score

    @property
    def current_hand(self) -> int:
        return self._current_hand

    @property
    def num_of_hands(self) -> int:
        return self._num_of_hands

    def new_hand(self):
        """Create new hand of cards."""
        self.hand = Hand(self.hand.bet)

    def split_hand(self):
        """Split current hand into two hands."""
        # verify player has enough money, else raise error
        if self.bank >= self.hand.bet:
            self._hand.append(Hand(self.hand.bet))
            self._num_of_hands += 1
            self._hand[self._num_of_hands].cards.append(self.hand.cards.pop())
        else:
            raise ValueError("Value Error: Not enough money to split hand!")

    def add_card(self, card_obj: Card, hand_num=None):
        if hand_num is None:
            self.hand.cards.append(card_obj)
        else:
            if 0 <= hand_num <= self._num_of_hands:
                self._hand[hand_num].cards.append(card_obj)
            else:
                raise IndexError("Index Error: hand_num out of range!")

    def next_hand(self):
        if self._current_hand < self._num_of_hands:
            self._current_hand += 1
        else:
            raise IndexError("Index Error: No More Player Hands!")
