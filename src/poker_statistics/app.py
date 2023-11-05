__author__ = "Eli Aviv"
__date__ = "24/10/2023"

import random

# from src.poker_statistics.model.Player import Player
from poker import Card, Hand

from src.poker_statistics.model.full_hand.full_hand import Player


def main():
    calculate_pre_flop_winning_percentage()


def calculate_pre_flop_winning_percentage():
    i = 0
    hands = list(Hand)

    while True:
        i += 1
        print(f'Game number #{i}\n')

        deck = list(Card)
        random.shuffle(deck)

        a = Player()
        b = Player()

        stating_combo1 = _create_random_starting_combo(hands)
        a.deal_starting_hand(stating_combo1)
        print(f'A starting hand: {stating_combo1}\n')

        stating_combo2 = _create_random_starting_combo(hands)
        b.deal_starting_hand(stating_combo2)
        print(f'B starting hand: {stating_combo2}\n')

        flop = [deck.pop() for __ in range(3)]
        print(f'Flop: {flop}\n')

        a.build_full_hand(flop)
        b.build_full_hand(flop)

        turn = [deck.pop()]
        print(f'Turn: {turn}\n')

        a.build_full_hand(turn)
        b.build_full_hand(turn)

        river = [deck.pop()]
        print(f'River: {river}\n')

        a.build_full_hand(river)
        b.build_full_hand(river)

        print(f'A rank: {a.full_hand.rank}\n')
        print(f'A cards: {a.full_hand.cards}\n')

        print(f'B rank: {b.full_hand.rank}\n')
        print(f'B cards: {b.full_hand.cards}\n')

        result = a.compare(b)
        if result == 1:
            print("A WINS!\n")
        elif result == -1:
            print("B WINS!\n")
        else:
            print("DRAW!\n")

        print(f"Game Finished #{i}\n")


def _create_random_starting_combo(hands):
    combo = random.choice(random.choice(hands).to_combos())
    return [combo.first, combo.second]


if __name__ == '__main__':
    main()
