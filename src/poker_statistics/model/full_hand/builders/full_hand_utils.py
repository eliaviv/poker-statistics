__author__ = "Eli Aviv"
__date__ = "04/11/2023"

import numpy as np


CARD_VAL_TO_REAL_VALUE = {
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


def find_all_cards_with_same_shape(cards):
    card_suits = [card.suit.val for card in cards]
    uniques, counts = np.unique(card_suits, return_counts=True)
    if 5 not in counts and 6 not in counts and 7 not in counts:
        return None

    flush_indices = np.where(card_suits == uniques[np.where(counts >= 5)[0]])
    reduced_cards = np.take(cards, flush_indices)[0]
    return reduced_cards


def find_five_cards_in_a_row(cards, value_index):
    sorted_cards = sorted(cards, key=lambda card: get_card_value(card, value_index))
    sorted_card_real_values = [get_card_value(card, value_index) for card in sorted_cards]
    unique_sorted_card_real_values, unique_indices = np.unique(sorted_card_real_values, return_index=True)
    reduced_sorted_cards = np.take(sorted_cards, unique_indices)

    at_least_five_ones_in_a_row_indices = find_at_least_five_ones_in_a_row(unique_sorted_card_real_values)
    if at_least_five_ones_in_a_row_indices is None:
        return None

    chosen_cards = np.take(reduced_sorted_cards, at_least_five_ones_in_a_row_indices)
    return chosen_cards


def find_at_least_five_ones_in_a_row(unique_sorted_card_real_values):
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


def find_high_card_index(cards):
    card_real_values = [get_card_value(card, 0) for card in cards]
    return np.where(card_real_values == np.max(card_real_values))[0][:1]


def get_card_value(card, value_index):
    return CARD_VAL_TO_REAL_VALUE[card.rank.val][value_index]
