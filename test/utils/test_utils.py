__author__ = "Eli Aviv"
__date__ = "07/11/2023"

import numpy as np
from poker import Suit, Rank, Card


def generate_same_suit_cards(num_of_same_suit, specific_suit=None):
    cards = []
    suit = Suit.make_random() if specific_suit is None else specific_suit
    for i in range(num_of_same_suit):
        rank = Rank.make_random()
        card = Card(rank.val + suit.val)
        while card in cards:
            rank = Rank.make_random()
            card = Card(rank.val + suit.val)
        cards.append(card)

    return cards


def generate_same_rank_cards(specific_ranks_and_amounts):
    cards = []
    for i in range(len(specific_ranks_and_amounts)):
        rank = specific_ranks_and_amounts[i][0]
        amount = specific_ranks_and_amounts[i][1]
        for j in range(amount):
            suit = Suit.make_random()
            card = Card(rank.val + suit.val)
            while card in cards:
                suit = Suit.make_random()
                card = Card(rank.val + suit.val)
            cards.append(card)

    return cards


def fill_with_random_cards(cards,
                           num_of_cards,
                           excluded_suits=[],
                           excluded_ranks=[],
                           max_amount_from_random_rank=None,
                           max_amount_from_random_suit=None):
    for i in range(num_of_cards):
        suit = Suit.make_random()
        card_suits = [card.suit for card in cards]
        uniques, counts = np.unique(card_suits, return_counts=True)
        uniques_dict = dict(zip(uniques, counts))
        while suit in excluded_suits or (suit in uniques_dict and uniques_dict[suit] == max_amount_from_random_suit):
            suit = Suit.make_random()

        rank = Rank.make_random()
        card_ranks = [card.rank for card in cards]
        uniques, counts = np.unique(card_ranks, return_counts=True)
        uniques_dict = dict(zip(uniques, counts))
        while rank in excluded_ranks or (rank in uniques_dict and uniques_dict[rank] == max_amount_from_random_rank):
            rank = Rank.make_random()

        card = Card(rank.val + suit.val)
        while card in cards:
            rank = Rank.make_random()
            card = Card(rank.val + suit.val)

        cards.append(card)
