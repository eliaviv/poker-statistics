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
    reduced_cards = _find_all_cards_with_same_shape(cards)
    if reduced_cards is None:
        return None

    chosen_cards = build_full_hand_with_straight(reduced_cards)
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
    reduced_cards = _find_all_cards_with_same_shape(cards)
    if reduced_cards is None:
        return None

    chosen_cards = sorted(reduced_cards, key=lambda card: VAL_TO_REAL_VALUE[card.rank.val][0])[-5:]
    return chosen_cards


def build_full_hand_with_straight(cards):
    chosen_cards = _find_five_cards_in_a_row(cards, 0)
    if chosen_cards is not None:
        return chosen_cards

    chosen_cards = _find_five_cards_in_a_row(cards, 1)
    if chosen_cards is None:
        return None

    return chosen_cards


def build_full_hand_with_three_of_a_kind(cards):
    card_vals = [card.rank.val for card in cards]
    uniques, counts = np.unique(card_vals, return_counts=True)

    if 3 not in counts:
        return None

    three_of_a_kind_indices = np.where(card_vals == uniques[np.where(counts == 3)[0]])
    chosen_cards = np.take(cards, three_of_a_kind_indices)
    reduced_cards = np.delete(cards, three_of_a_kind_indices)

    for i in range(0, 2):
        high_card_index = _find_high_card_index(reduced_cards)
        chosen_cards = np.append(chosen_cards, np.take(reduced_cards, high_card_index))
        reduced_cards = np.delete(reduced_cards, high_card_index)

    return chosen_cards


def build_full_hand_with_two_pair(cards):
    card_vals = [card.rank.val for card in cards]
    uniques, counts = np.unique(card_vals, return_counts=True)
    counts_uniques, counts_counts = np.unique(counts, return_counts=True)
    counts_uniques_dict = dict(zip(counts_uniques, counts_counts))

    if 2 not in counts_uniques_dict:
        return None

    if counts_uniques_dict[2] < 2:
        return None

    first_pair_indices = np.where(card_vals == np.array(str(uniques[np.where(counts == 2)[0]][0])))[0]
    second_pair_indices = np.where(card_vals == np.array(str(uniques[np.where(counts == 2)[0]][1])))[0]

    if counts_uniques_dict[2] == 2:
        chosen_cards = np.take(cards, first_pair_indices)
        chosen_cards = np.append(chosen_cards, np.take(cards, second_pair_indices))
        reduced_cards = np.delete(cards, np.flatnonzero(np.isin(cards, chosen_cards)))
        chosen_cards = np.append(chosen_cards, np.take(reduced_cards, _find_high_card_index(reduced_cards)))
        return chosen_cards

    if VAL_TO_REAL_VALUE[card_vals[first_pair_indices[0]]][0] > VAL_TO_REAL_VALUE[card_vals[second_pair_indices[0]]][0]:
        chosen_cards = np.take(cards, first_pair_indices)
        reduced_cards = np.delete(cards, first_pair_indices)
        left_pair = second_pair_indices
    else:
        chosen_cards = np.take(cards, second_pair_indices)
        reduced_cards = np.delete(cards, second_pair_indices)
        left_pair = first_pair_indices

    third_pair_indices = np.where(card_vals == np.array(str(uniques[np.where(counts == 2)[0]][2])))[0]

    if VAL_TO_REAL_VALUE[card_vals[left_pair[0]]][0] > VAL_TO_REAL_VALUE[card_vals[third_pair_indices[0]]][0]:
        chosen_cards = np.append(chosen_cards, np.take(cards, left_pair))
        reduced_cards = np.delete(cards, np.flatnonzero(np.isin(cards, chosen_cards)))
    else:
        chosen_cards = np.append(chosen_cards, np.take(cards, third_pair_indices))
        reduced_cards = np.delete(cards, np.flatnonzero(np.isin(cards, chosen_cards)))

    chosen_cards = np.append(chosen_cards, np.take(reduced_cards, _find_high_card_index(reduced_cards)))
    return chosen_cards


def build_full_hand_with_pair(cards):
    card_vals = [card.rank.val for card in cards]
    uniques, counts = np.unique(card_vals, return_counts=True)

    if 2 not in counts:
        return None

    pair_indices = np.where(card_vals == uniques[np.where(counts == 2)[0]])
    chosen_cards = np.take(cards, pair_indices)
    reduced_cards = np.delete(cards, pair_indices)

    for i in range(0, 3):
        high_card_index = _find_high_card_index(reduced_cards)
        chosen_cards = np.append(chosen_cards, np.take(reduced_cards, high_card_index))
        reduced_cards = np.delete(reduced_cards, high_card_index)

    return chosen_cards


def build_full_hand_with_high_card(cards):
    reduced_cards = cards
    chosen_cards = np.array([])
    for i in range(0, 5):
        high_card_index = _find_high_card_index(reduced_cards)
        chosen_cards = np.append(chosen_cards, np.take(reduced_cards, high_card_index))
        reduced_cards = np.delete(reduced_cards, high_card_index)

    return chosen_cards


def _find_all_cards_with_same_shape(cards):
    card_suits = [card.suit.val for card in cards]
    uniques, counts = np.unique(card_suits, return_counts=True)
    if 5 not in counts and 6 not in counts and 7 not in counts:
        return None

    flush_indices = np.where(card_suits == uniques[np.where(counts >= 5)[0]])
    reduced_cards = np.take(cards, flush_indices)[0]
    return reduced_cards


def _find_five_cards_in_a_row(cards, value_index):
    sorted_cards = sorted(cards, key=lambda card: VAL_TO_REAL_VALUE[card.rank.val][value_index])
    sorted_card_real_values = [VAL_TO_REAL_VALUE[card.rank.val][value_index] for card in sorted_cards]
    unique_sorted_card_real_values, unique_indices = np.unique(sorted_card_real_values, return_index=True)
    reduced_sorted_cards = np.take(sorted_cards, unique_indices)

    at_least_five_ones_in_a_row_indices = _find_at_least_five_ones_in_a_row(unique_sorted_card_real_values)
    if at_least_five_ones_in_a_row_indices is None:
        return None

    chosen_cards = np.take(reduced_sorted_cards, at_least_five_ones_in_a_row_indices)
    return chosen_cards


def _find_at_least_five_ones_in_a_row(unique_sorted_card_real_values):
    unique_sorted_card_real_values_diffs = np.diff(unique_sorted_card_real_values)

    if 1 not in unique_sorted_card_real_values_diffs:
        return None

    diff_indices = np.array([], dtype=int)
    for i in range(0, unique_sorted_card_real_values_diffs.size):
        if unique_sorted_card_real_values_diffs[i] == 1:
            diff_indices = np.append(diff_indices, i)
        else:
            diff_indices = np.array([])

        if diff_indices.size >= 4:
            break

    if diff_indices.size < 4:
        return None

    for i in range(diff_indices.size, unique_sorted_card_real_values_diffs.size):
        if unique_sorted_card_real_values_diffs[i] == 1:
            diff_indices = np.append(diff_indices, i)
        else:
            break

    indices = set()
    for i in diff_indices:
        indices.add(i)
        indices.add(i + 1)

    return list(indices)


def _find_high_card_index(cards):
    card_real_values = [VAL_TO_REAL_VALUE[card.rank.val][0] for card in cards]
    return np.where(card_real_values == np.max(card_real_values))[0][:1]
