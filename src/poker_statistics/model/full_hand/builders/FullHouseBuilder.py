__author__ = "Eli Aviv"
__date__ = "04/11/2023"

import numpy as np

from src.poker_statistics.model.full_hand.Rank import Rank
from src.poker_statistics.model.full_hand.builders.FullHandBuilder import FullHandBuilder
from src.poker_statistics.model.full_hand.builders.builder_utils import CARD_VAL_TO_REAL_VALUE, get_card_value


class FullHouseBuilder(FullHandBuilder):
    def build(self, cards):
        card_vals = [card.rank.val for card in cards]
        uniques, counts = np.unique(card_vals, return_counts=True)
        counts_uniques, counts_counts = np.unique(counts, return_counts=True)
        counts_uniques_dict = dict(zip(counts_uniques, counts_counts))

        if 3 not in counts_uniques_dict:
            self.cards = None
            return

        if counts_uniques_dict[3] == 2:
            first_three_of_a_kind_indices = np.where(card_vals == np.array(str(uniques[np.where(counts == 3)[0]][0])))[0]
            second_three_of_a_kind_indices = np.where(card_vals == np.array(str(uniques[np.where(counts == 3)[0]][1])))[0]
            if CARD_VAL_TO_REAL_VALUE[card_vals[first_three_of_a_kind_indices[0]]][0] > \
                    CARD_VAL_TO_REAL_VALUE[card_vals[second_three_of_a_kind_indices[0]]][0]:
                chosen_cards = np.take(cards, first_three_of_a_kind_indices)
                reduced_cards = np.delete(cards, first_three_of_a_kind_indices)
            else:
                chosen_cards = np.take(cards, second_three_of_a_kind_indices)
                reduced_cards = np.delete(cards, second_three_of_a_kind_indices)

            chosen_cards = np.append(chosen_cards, reduced_cards[:2])
            self.cards = chosen_cards
            return

        if 2 not in counts_uniques_dict:
            self.cards = None
            return

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
            self.cards = chosen_cards
            return

        pair_indices = np.where(card_vals == uniques[np.where(counts == 2)[0]])
        chosen_cards = np.append(chosen_cards, np.take(cards, pair_indices))

        self.cards = chosen_cards

    def rank(self):
        return Rank.FULL_HOUSE

    def compare(self, other_cards):
        this_card_vals = [card.rank.val for card in self.cards]
        this_uniques, this_counts = np.unique(this_card_vals, return_counts=True)
        this_three_of_a_kind_indices = np.where(this_card_vals == this_uniques[np.where(this_counts == 3)[0]])[0]

        other_card_vals = [card.rank.val for card in other_cards]
        other_uniques, other_counts = np.unique(other_card_vals, return_counts=True)
        other_three_of_a_kind_indices = np.where(other_card_vals == other_uniques[np.where(other_counts == 3)[0]])[0]

        if get_card_value(self.cards[this_three_of_a_kind_indices[0]], 0) > get_card_value(other_cards[other_three_of_a_kind_indices[0]], 0):
            return 1
        if get_card_value(self.cards[this_three_of_a_kind_indices[0]], 0) < get_card_value(other_cards[other_three_of_a_kind_indices[0]], 0):
            return -1

        this_reduced_cards = np.delete(self.cards, this_three_of_a_kind_indices)
        other_reduced_cards = np.delete(other_cards, other_three_of_a_kind_indices)

        if get_card_value(this_reduced_cards[0], 0) > get_card_value(other_reduced_cards[0], 0):
            return 1
        if get_card_value(this_reduced_cards[0], 0) < get_card_value(other_reduced_cards[0], 0):
            return -1

        return 0
