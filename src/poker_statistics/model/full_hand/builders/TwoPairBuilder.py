__author__ = "Eli Aviv"
__date__ = "04/11/2023"

import numpy as np

from src.poker_statistics.model.full_hand.builders.FullHandBuilder import FullHandBuilder
from src.poker_statistics.model.full_hand.builders.builder_utils import CARD_VAL_TO_REAL_VALUE, find_high_card_index


class TwoPairBuilder(FullHandBuilder):
    def build(self, cards):
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
            chosen_cards = np.append(chosen_cards, np.take(reduced_cards, find_high_card_index(reduced_cards)))
            return chosen_cards

        if CARD_VAL_TO_REAL_VALUE[card_vals[first_pair_indices[0]]][0] > \
                CARD_VAL_TO_REAL_VALUE[card_vals[second_pair_indices[0]]][0]:
            chosen_cards = np.take(cards, first_pair_indices)
            left_pair = second_pair_indices
        else:
            chosen_cards = np.take(cards, second_pair_indices)
            left_pair = first_pair_indices

        third_pair_indices = np.where(card_vals == np.array(str(uniques[np.where(counts == 2)[0]][2])))[0]

        if CARD_VAL_TO_REAL_VALUE[card_vals[left_pair[0]]][0] > \
                CARD_VAL_TO_REAL_VALUE[card_vals[third_pair_indices[0]]][0]:
            chosen_cards = np.append(chosen_cards, np.take(cards, left_pair))
            reduced_cards = np.delete(cards, np.flatnonzero(np.isin(cards, chosen_cards)))
        else:
            chosen_cards = np.append(chosen_cards, np.take(cards, third_pair_indices))
            reduced_cards = np.delete(cards, np.flatnonzero(np.isin(cards, chosen_cards)))

        chosen_cards = np.append(chosen_cards, np.take(reduced_cards, find_high_card_index(reduced_cards)))

        return chosen_cards
