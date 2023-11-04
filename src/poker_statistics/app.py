__author__ = "Eli Aviv"
__date__ = "24/10/2023"

import random

# from src.poker_statistics.model.Player import Player
from poker import Card

from src.poker_statistics.model.full_hand.full_hand import FullHand


def main():
    calculate_pre_flop_winning_percentage()


def calculate_pre_flop_winning_percentage():
    i = 0
    deck = list(Card)
    while True:
        random.shuffle(deck)
        print(deck[:7])
        a = FullHand(deck[:7])
        print(f'a rank: {a.builder.rank}')
        print(f'a cards: {a.builder.cards}')

        random.shuffle(deck)
        print(deck[:7])
        b = FullHand(deck[:7])
        print(f'b rank: {b.builder.rank}')
        print(f'b cards: {b.builder.cards}')

        result = a.compare(b)
        if result == 1:
            print("a wins!")
        elif result == -1:
            print("b wins!")
        else:
            print("draw!")

        print()

        i += 1
        print(i)


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
