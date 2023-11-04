__author__ = "Eli Aviv"
__date__ = "04/11/2023"

import numpy as np

from src.poker_statistics.model.full_hand.builders.FullHandBuilder import FullHandBuilder
from src.poker_statistics.model.full_hand.builders.builder_utils import CARD_VAL_TO_REAL_VALUE


class FullHouseBuilder(FullHandBuilder):
    def build(self, cards):
        card_vals = [card.rank.val for card in cards]
        uniques, counts = np.unique(card_vals, return_counts=True)
        counts_uniques, counts_counts = np.unique(counts, return_counts=True)
        counts_uniques_dict = dict(zip(counts_uniques, counts_counts))

        if 3 not in counts_uniques_dict:
            return None

        if counts_uniques_dict[3] == 2:
            first_three_of_a_kind_indices = np.where(card_vals == np.array(str(uniques[np.where(counts == 3)[0]][0])))[
                0]
            second_three_of_a_kind_indices = np.where(card_vals == np.array(str(uniques[np.where(counts == 3)[0]][1])))[
                0]
            if CARD_VAL_TO_REAL_VALUE[card_vals[first_three_of_a_kind_indices[0]]][0] > \
                    CARD_VAL_TO_REAL_VALUE[card_vals[second_three_of_a_kind_indices[0]]][0]:
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
            if CARD_VAL_TO_REAL_VALUE[card_vals[first_pair_indices[0]]][0] > \
                    CARD_VAL_TO_REAL_VALUE[card_vals[second_pair_indices[0]]][0]:
                chosen_cards = np.append(chosen_cards, np.take(cards, first_pair_indices))
            else:
                chosen_cards = np.append(chosen_cards, np.take(cards, second_pair_indices))
            return chosen_cards

        pair_indices = np.where(card_vals == uniques[np.where(counts == 2)[0]])
        chosen_cards = np.append(chosen_cards, np.take(cards, pair_indices))

        return chosen_cards
