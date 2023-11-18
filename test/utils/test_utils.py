__author__ = "Eli Aviv"
__date__ = "07/11/2023"

import random

import numpy as np
from poker import Suit, Rank, Card

from poker_statistics.model.full_hand.full_hand_utils import get_card_value, find_high_card_index, \
    get_rank_val_value, get_rank_value_val


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


def generate_straight_cards(num_of_cards, specific_suit=None):
    cards = []

    rank = Rank.make_random()
    suit = Suit.make_random() if specific_suit is None else specific_suit
    cards.append(Card(rank.val + suit.val))
    num_of_cards -= 1

    rank_value = get_rank_val_value(rank, 0)
    rank_value_right = rank_value + 1
    rank_value_left = rank_value - 1
    while num_of_cards > 0:
        if num_of_cards % 2 == 0:
            if rank_value_right <= 14:
                rank = Rank(get_rank_value_val(rank_value_right))
                rank_value_right += 1
            else:
                rank = Rank(get_rank_value_val(rank_value_left))
                rank_value_left -= 1
        else:
            if rank_value_left >= 1:
                rank = Rank(get_rank_value_val(rank_value_left))
                rank_value_left -= 1
            else:
                rank = Rank(get_rank_value_val(rank_value_right))
                rank_value_right += 1

        suit = Suit.make_random() if specific_suit is None else specific_suit
        cards.append(Card(rank.val + suit.val))
        num_of_cards -= 1

    random.shuffle(cards)

    return cards


def fill_with_random_cards(cards,
                           num_of_cards,
                           excluded_suits=[],
                           excluded_ranks=[],
                           max_amount_from_random_rank=None,
                           max_amount_from_random_suit=None):
    for i in range(num_of_cards):
        card = _generate_random_card(cards, excluded_suits, excluded_ranks, max_amount_from_random_rank,
                                     max_amount_from_random_suit)
        while card in cards:
            card = _generate_random_card(cards, excluded_suits, excluded_ranks, max_amount_from_random_rank,
                                         max_amount_from_random_suit)

        cards.append(card)


def assert_by_high_card(cards, other_cards, excluded_cards, other_excluded_cards, result):
    reduced_cards = np.delete(cards, np.flatnonzero(np.isin(cards, excluded_cards)))
    other_reduced_cards = np.delete(other_cards, np.flatnonzero(np.isin(other_cards, other_excluded_cards)))
    high_card_index = find_high_card_index(reduced_cards)[0]
    other_high_card_index = find_high_card_index(other_reduced_cards)[0]
    if get_card_value(reduced_cards[high_card_index], 0) == get_card_value(other_reduced_cards[other_high_card_index],
                                                                           0):
        if len(reduced_cards) == 1:
            assert result == 0
        else:
            assert_by_high_card(np.delete(reduced_cards, high_card_index),
                                np.delete(other_reduced_cards, other_high_card_index),
                                np.append(excluded_cards, reduced_cards[high_card_index]),
                                np.append(other_excluded_cards, other_reduced_cards[other_high_card_index]),
                                result)
    elif get_card_value(reduced_cards[high_card_index], 0) > get_card_value(other_reduced_cards[other_high_card_index],
                                                                            0):
        assert result == 1
    else:
        assert result == -1


def _generate_random_card(cards,
                          excluded_suits=[],
                          excluded_ranks=[],
                          max_amount_from_random_rank=None,
                          max_amount_from_random_suit=None):
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

    return Card(rank.val + suit.val)
