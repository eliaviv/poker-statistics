__author__ = "Eli Aviv"
__date__ = "24/10/2023"

import random

# from src.poker_statistics.model.Player import Player
import src.poker_statistics.model.full_hand.rank
from poker import Card


def main():
    calculate_pre_flop_winning_percentage()


def calculate_pre_flop_winning_percentage():
    while True:
        deck = list(Card)
        random.shuffle(deck)
        a = src.poker_statistics.model.full_hand.full_hand.rank.build_full_hand_with_two_pair(deck[:7])

    #
    # hands = list(Hand)
    # stating_combo1 = _create_random_starting_combo(hands)
    # player1 = Player()
    # player1.starting_hand = stating_combo1
    #
    # stating_combo2 = _create_random_starting_combo(hands)
    # player2 = Player()
    # player2.starting_hand = stating_combo2
    #
    # combo = Combo("AdAs")
    #
    # flop = [deck.pop() for __ in range(3)]
    # turn = deck.pop()
    # river = deck.pop()
    #
    # print(Hand('AA'))
    #
    # print('eli')


def _create_random_starting_combo(hands):
    return random.choice(random.choice(hands).to_combos())


if __name__ == '__main__':
    main()
