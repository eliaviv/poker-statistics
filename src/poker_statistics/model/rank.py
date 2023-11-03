__author__ = "Eli Aviv"
__date__ = "24/10/2023"
__copyright__ = "Copyright (C) 2023 IXDen (https://www.ixden.com)"

from enum import Enum

import numpy as np
from poker import Card


class FullHand:
    pass


class FullHandRank(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8


VAL_TO_REAL_VALUE = {
    '1': (1, 1),
    '2': (2, 2),
    '3': (3, 3),
    '4': (4, 4),
    '5': (5, 5),
    '6': (6, 6),
    '7': (7, 7),
    '8': (8, 8),
    '9': (9, 9),
    'T': (10, 10),
    'J': (11, 11),
    'Q': (12, 12),
    'K': (13, 13),
    'A': (14, 1)
}


def build_full_hand_with_straight_flush(cards):
    chosen_cards = build_full_hand_with_flush(cards)
    if chosen_cards is None:
        return None

    chosen_cards = build_full_hand_with_straight(chosen_cards)
    if chosen_cards is None:
        return None

    return chosen_cards


def build_full_hand_with_four_of_a_kind(cards):
    card_vals = [card.rank.val for card in cards]
    uniques, counts = np.unique(card_vals, return_counts=True)

    if 4 not in counts:
        return None

    four_of_a_kind_indices = np.where(card_vals == uniques[np.where(counts == 4)[0]])
    chosen_cards = np.take(cards, four_of_a_kind_indices)
    reduced_cards = np.delete(cards, four_of_a_kind_indices)
    chosen_cards = np.append(chosen_cards, np.take(reduced_cards, _find_high_card_index(reduced_cards)))
    return chosen_cards


def build_full_hand_with_full_house(cards):
    card_vals = [card.rank.val for card in cards]
    uniques, counts = np.unique(card_vals, return_counts=True)
    counts_uniques, counts_counts = np.unique(counts, return_counts=True)
    counts_uniques_dict = dict(zip(counts_uniques, counts_counts))

    if 3 not in counts_uniques_dict:
        return None

    if counts_uniques_dict[3] == 2:
        first_three_of_a_kind_indices = np.where(card_vals == np.array(str(uniques[np.where(counts == 3)[0]][0])))[0]
        second_three_of_a_kind_indices = np.where(card_vals == np.array(str(uniques[np.where(counts == 3)[0]][1])))[0]
        if VAL_TO_REAL_VALUE[card_vals[first_three_of_a_kind_indices[0]]][0] > VAL_TO_REAL_VALUE[card_vals[second_three_of_a_kind_indices[0]]][0]:
            chosen_cards = np.take(cards, first_three_of_a_kind_indices)
            reduced_cards = np.delete(cards, first_three_of_a_kind_indices)
        else:
            chosen_cards = np.take(cards, second_three_of_a_kind_indices)
            reduced_cards = np.delete(cards, second_three_of_a_kind_indices)

        chosen_cards = np.append(chosen_cards, reduced_cards[:2])
        return chosen_cards

    if 2 not in counts_uniques_dict:
        return None

    three_of_a_kind_indices = np.where(card_vals == uniques[np.where(counts == 3)[0]])
    chosen_cards = np.take(cards, three_of_a_kind_indices)

    if counts_uniques_dict[2] == 2:
        first_pair_indices = np.where(card_vals == np.array(str(uniques[np.where(counts == 2)[0]][0])))[0]
        second_pair_indices = np.where(card_vals == np.array(str(uniques[np.where(counts == 2)[0]][1])))[0]
        if VAL_TO_REAL_VALUE[card_vals[first_pair_indices[0]]][0] > VAL_TO_REAL_VALUE[card_vals[second_pair_indices[0]]][0]:
            chosen_cards = np.append(chosen_cards, np.take(cards, first_pair_indices))
        else:
            chosen_cards = np.append(chosen_cards, np.take(cards, second_pair_indices))
        return chosen_cards

    pair_indices = np.where(card_vals == uniques[np.where(counts == 2)[0]])
    chosen_cards = np.append(chosen_cards, np.take(cards, pair_indices))
    return chosen_cards


def build_full_hand_with_flush(cards):
    card_suits = [card.suit.val for card in cards]
    uniques, counts = np.unique(card_suits, return_counts=True)
    if 5 not in counts and 6 not in counts and 7 not in counts:
        return None

    flush_indices = np.where(card_suits == uniques[np.where(counts >= 5)[0]])
    reduced_cards = np.take(cards, flush_indices)[0]

    chosen_cards = sorted(reduced_cards, key=lambda card: VAL_TO_REAL_VALUE[card.rank.val][0])[-5:]
    return chosen_cards


def build_full_hand_with_straight(cards):
    for i in range(0, 1):
        sorted_cards = sorted(cards, key=lambda card: VAL_TO_REAL_VALUE[card.rank.val][0])
        sorted_card_real_values = [VAL_TO_REAL_VALUE[card.rank.val][i] for card in sorted_cards]
        sorted_card_real_values_diffs = np.diff(np.sort(sorted_card_real_values))

        if 1 not in sorted_card_real_values_diffs:
            return None

        ones_in_a_row, straight_last_index = _find_at_least_five_ones_in_a_row(sorted_card_real_values_diffs)
        if ones_in_a_row < 4:
            return None

        chosen_cards = sorted_cards[straight_last_index - 4:straight_last_index + 1]
        return chosen_cards


def build_full_hand_with_three_of_a_kind(cards):
    for i in range(0, 1):
        sorted_cards = sorted(cards, key=lambda card: VAL_TO_REAL_VALUE[card.rank.val][0])
        sorted_card_real_values = [VAL_TO_REAL_VALUE[card.rank.val][i] for card in sorted_cards]
        sorted_card_real_values_diffs = np.diff(np.sort(sorted_card_real_values))

        if 1 not in sorted_card_real_values_diffs:
            return None

        ones_in_a_row, straight_last_index = _find_at_least_five_ones_in_a_row(sorted_card_real_values_diffs)
        if ones_in_a_row < 4:
            return None

        chosen_cards = sorted_cards[straight_last_index - 4:straight_last_index + 1]
        return chosen_cards


def _find_high_card_index(cards):
    card_real_values = [VAL_TO_REAL_VALUE[card.rank.val][0] for card in cards]
    return np.where(card_real_values == np.max(card_real_values))[0][:1]


def _find_at_least_five_ones_in_a_row(sorted_card_real_values_diffs):
    # sorted_card_real_values_diffs = np.array([1,1,1,1])
    ones_in_a_row = 0
    index = 0
    for i in range(0, sorted_card_real_values_diffs.size):
        if sorted_card_real_values_diffs[i] == 1:
            ones_in_a_row += 1
        else:
            ones_in_a_row = 0

        if ones_in_a_row >= 4:
            index = i
            break

    if ones_in_a_row < 4:
        return ones_in_a_row, index

    final_index = index
    for i in range(index + 1, sorted_card_real_values_diffs.size):
        if sorted_card_real_values_diffs[i] == 1:
            ones_in_a_row += 1
            final_index = i
        else:
            break

    return ones_in_a_row, final_index + 1




