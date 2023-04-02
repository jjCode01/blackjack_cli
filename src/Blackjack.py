"""Blackjack Game"""
from src.Deck import Deck
from Player import Player
from os import system, name
import time
import datetime


def get_player_name() -> str:
    new_player_name = input("Enter your name: ")
    return new_player_name if not new_player_name == "" else "Player"


class Blackjack:
    def __init__(self):
        """Initialize Blackjack game object."""
        self.deck = Deck(num_of_decks=2, shuffled=True)

        self.player = Player("Player", 100.0, 5.0)
        self.dealer = Player("Dealer", 0.0, 0.0)

        self.bet_multiplier = 1.0  # Multiplier for blackjack and double down
        self.plays = 0
        self.result = None

    def refresh_table(self):
        """Redraws the game in the terminal."""
        clear()

        # Display Dealer and Player Hands
        print(f"{self.dealer}\n{self.player}\n{'-' * 60}")

        # Display Player Money and Bet Amount
        print(
            f"Money:\t${self.player.money}\n"
            f"Bet:\t${self.player.hand.bet * self.bet_multiplier}\n"
        )

    def start(self):
        """Starts game play.  Prompts player for their name and bet amount."""
        clear()
        print(f"\n\n      ♥♦♣♠ BLACKJACK ♠♣♦♥\n{'_' * 31}\n")

        self.player.name = get_player_name()
        self.player.hand.bet = float(
            input(f"You have {self.player.money}, how much would you like to bet? ")
        )

        self.play()

    def play(self):
        """Loops game play until player runs out of money, or player chooses to quit."""

        def display_game_play_options():
            """Present game play options to Player and perform game play based on Players input."""

            def get_players_input():
                """
                Present game play options to Player
                :return: Players input
                :rtype: str
                """
                _option_selected = None  # variable to hold Players input

                # check game conditions to allow double down and/or split
                if (
                    len(self.player.hand) == 2
                    and self.player.bank >= self.player.hand.bet
                ):
                    # Player has enough money and is new hand

                    # check if card faces match to allow hand to be split
                    if self.player.hand.cards[0].face == self.player.hand.cards[1].face:

                        # Player can split hand, include option in menu
                        temp_choice = input(
                            "Enter h and press enter to Hit\n"
                            "Enter d and press enter to Double Down\n"
                            "Enter s and press enter to Split\n"
                            "Press enter to stay\n"
                            ": "
                        ).lower()

                        # verify players input is valid
                        if (
                            temp_choice == "h"
                            or temp_choice == "d"
                            or temp_choice == "s"
                        ):
                            _option_selected = temp_choice

                    else:
                        # Player cannot split hand
                        temp_choice = input(
                            "Enter h and press enter to Hit\n"
                            "Enter d and press enter to Double Down\n"
                            "Press enter to stay\n"
                            ": "
                        ).lower()

                        # verify players input is valid
                        if temp_choice == "h" or temp_choice == "d":
                            _option_selected = temp_choice
                else:
                    # player can only hit or stay
                    temp_choice = input(
                        "Enter h and press enter to Hit\n" "Press enter to stay\n" ": "
                    ).lower()

                    # verify players input is valid
                    if temp_choice == "h":
                        _option_selected = temp_choice

                return _option_selected

            # promp Player for input based on available game play options
            _choice = get_players_input()

            # player chooses to Split Hand
            if _choice == "s":
                # split cards into 2 hands
                self.player.split_hand()

                # add card to original hand
                self.player.add_card(card_obj=self.deck.deal_card())
                # add card to new hand
                self.player.add_card(
                    card_obj=self.deck.deal_card(), hand_num=self.player.num_of_hands
                )

                # refresh screen and display choices
                self.refresh_table()
                display_game_play_options()

            # player chooses to Double Down
            elif _choice == "d":
                # double player bet
                self.bet_multiplier = 2.0  # REMOVE THIS LINE OF CODE
                self.player.hand.bet_multiplier = 2.0

                # add card to player hand and refresh screen
                self.player.add_card(self.deck.deal_card())
                self.refresh_table()

            # player chooses to Hit
            elif _choice == "h":
                # add card to player hand
                self.player.add_card(self.deck.deal_card())

                # refresh screen and continue playing
                self.refresh_table()

                # continue loop while Player hits and hand is less than 21
                while self.player.score < 21 and get_players_input() == "h":
                    # player hit: add card to hand
                    self.player.add_card(self.deck.deal_card())
                    self.refresh_table()

        # Loop game play until player runs out of money
        while self.player.money > 0:
            self.plays += 1
            self.bet_multiplier = 1.0

            # Check if Deck has enough cards to continue play
            # make new deck if below 15 cards
            if len(self.deck) < 15:
                self.deck = Deck(num_of_decks=2, shuffled=True)
                # self.deck.shuffle_new(num_of_decks=2)
                clear()
                print(f"Shuffling Deck....")
                time.sleep(0.5)
            else:
                clear()

            # check if player has enough money for current bet
            if self.player.hand.bet > self.player.money:
                self.player.hand.bet = self.player.money

            print("Dealing Cards....")
            time.sleep(0.5)

            # reset player and dealer hands
            self.player.new_hand()
            self.dealer.new_hand()

            # deal 2 cards to dealer and player
            for x in range(2):
                self.player.add_card(self.deck.deal_card())
                self.dealer.add_card(self.deck.deal_card())

            # check if dealer of player has blackjack
            if self.dealer.score == 21 or self.player.score == 21:
                # someone has blackjack; game play for hand is over
                self.refresh_table()
                self.game_over()
            else:
                # no one has blackjack; change dealers 2nd card to be face down
                self.dealer.hand.cards[1].flip()
                self.refresh_table()

                # initiate game play based on player input
                display_game_play_options()

                # check if player has multiple hands of cards
                if self.player.current_hand < self.player.num_of_hands:
                    input("Press Enter to continue to next hand...")
                    self.player.next_hand()
                    self.refresh_table()

                    # check if next hand is blackjack
                    if self.player.score < 21:
                        display_game_play_options()

                # check if player hand exceeded 21
                if 21 >= self.player.min_score > self.dealer.score:
                    self.dealer.hand.cards[1].flip()
                    while self.dealer.score < 16:
                        self.dealer.add_card(self.deck.deal_card())
                    self.refresh_table()

                self.game_over()

            # check if player still has money
            if self.player.money > 0:  # player still has money
                print("\nEnter q and press enter to quite")
                print("Enter b and press enter to change bet and continue")
                print("Press enter to keep playing\n")
                player_choice = input(": ")

                if player_choice.lower() == "q":
                    clear()
                    print(f"\nLeaving Game...")
                    time.sleep(0.5)
                    break
                elif player_choice == "b":
                    self.player.hand.bet = float(
                        input(
                            f"You have {self.player.money}, "
                            f"how much would you like to bet? "
                        )
                    )
            else:  # player is out of money
                # game session over - player is out of money
                clear()
                print(f"\nGame Over... You are out of money")
                time.sleep(0.5)

        clear()
        # self.display_stats()

    # function - game play for current hand ended
    # calculate who won and display the results
    def game_over(self):
        dealer_score = self.dealer.score

        # Record current date and time
        now = datetime.datetime.now()

        for h in self.player.hands:
            self.refresh_table()

            # function - draw banner of game results
            def draw_banner(banner):
                spc = " " * 10
                print(
                    f"{spc}┌{'─' * (10 + len(banner))}┐\n"
                    f"{spc}|     {banner}     |\n"
                    f"{spc}└{'─' *(10 + len(banner))}┘"
                )

            # function - player wins
            def win():
                self.player.money += self.player.hand.bet * h.bet_multiplier
                self.refresh_table()
                draw_banner("WINNER!")
                self.result = "Win"

            # function - player loses
            def lose():
                self.player.money -= self.player.hand.bet * h.bet_multiplier
                self.refresh_table()
                draw_banner("YOU LOSE")
                self.result = "Lose"

            def draw():
                self.refresh_table()
                draw_banner("DRAW")
                self.result = "Draw"

            player_score = h.score

            # Calculate who won the game
            if player_score == 21 and len(h) == 2:
                if dealer_score == 21 and len(self.dealer.hand) == 2:
                    draw()
                else:
                    h.bet_multiplier = 1.5
                    win()
            elif player_score > 21:  # player bust
                lose()
            elif dealer_score > 21:  # dealer bust
                win()
            else:  # neither player nor dealer bust
                if player_score > dealer_score:  # player win
                    win()
                elif player_score < dealer_score:  # dealer win
                    lose()
                else:  # game is a draw
                    draw()

            if len(self.player.hands) > 1:
                time.sleep(2.5)


def clear():
    """Clear terminal"""
    # 'nt' = windows; 'posix' = linux or mac
    _ = system("cls") if name == "nt" else system("clear")
