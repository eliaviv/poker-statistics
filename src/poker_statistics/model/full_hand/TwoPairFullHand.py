__author__ = "Eli Aviv"
__date__ = "04/11/2023"

import numpy as np

from src.poker_statistics.model.full_hand.Rank import Rank
from src.poker_statistics.model.full_hand.FullHand import FullHand
from src.poker_statistics.model.full_hand.full_hand_utils import CARD_VAL_TO_REAL_VALUE, find_high_card_index, \
    get_card_value


class TwoPairFullHand(FullHand):
    def build(self, cards):
        card_vals = [card.rank.val for card in cards]
        uniques, counts = np.unique(card_vals, return_counts=True)
        counts_uniques, counts_counts = np.unique(counts, return_counts=True)
        counts_uniques_dict = dict(zip(counts_uniques, counts_counts))

        if 2 not in counts_uniques_dict:
            self.cards = None
            return

        if counts_uniques_dict[2] < 2:
            self.cards = None
            return

        first_pair_indices = np.where(card_vals == np.array(str(uniques[np.where(counts == 2)[0]][0])))[0]
        second_pair_indices = np.where(card_vals == np.array(str(uniques[np.where(counts == 2)[0]][1])))[0]

        if counts_uniques_dict[2] == 2:
            chosen_cards = np.take(cards, first_pair_indices)
            chosen_cards = np.append(chosen_cards, np.take(cards, second_pair_indices))
            reduced_cards = np.delete(cards, np.flatnonzero(np.isin(cards, chosen_cards)))
            chosen_cards = np.append(chosen_cards, np.take(reduced_cards, find_high_card_index(reduced_cards)))
            self.cards = list(chosen_cards)
            return

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

        self.cards = list(chosen_cards)

    def rank(self):
        return Rank.TWO_PAIR

    def compare(self, other_cards):
        this_card_vals = [card.rank.val for card in self.cards]
        this_uniques, this_counts = np.unique(this_card_vals, return_counts=True)
        this_first_pair_indices = np.where(this_card_vals == np.array(str(this_uniques[np.where(this_counts == 2)[0]][0])))[0]
        this_second_pair_indices = np.where(this_card_vals == np.array(str(this_uniques[np.where(this_counts == 2)[0]][1])))[0]
        this_higher_and_lower_pair_indices_tuple = (this_first_pair_indices, this_second_pair_indices) if \
            get_card_value(self.cards[this_first_pair_indices[0]], 0) > get_card_value(self.cards[this_second_pair_indices[0]], 0) else \
            (this_second_pair_indices, this_first_pair_indices)

        other_card_vals = [card.rank.val for card in other_cards]
        other_uniques, other_counts = np.unique(other_card_vals, return_counts=True)
        other_first_pair_indices = np.where(other_card_vals == np.array(str(other_uniques[np.where(other_counts == 2)[0]][0])))[0]
        other_second_pair_indices = np.where(other_card_vals == np.array(str(other_uniques[np.where(other_counts == 2)[0]][1])))[0]
        other_higher_and_lower_pair_indices_tuple = (other_first_pair_indices, other_second_pair_indices) if \
            get_card_value(other_cards[other_first_pair_indices[0]], 0) > get_card_value(other_cards[other_second_pair_indices[0]], 0) else \
            (other_second_pair_indices, other_first_pair_indices)

        if get_card_value(self.cards[this_higher_and_lower_pair_indices_tuple[0][0]], 0) > get_card_value(other_cards[other_higher_and_lower_pair_indices_tuple[0][0]], 0):
            return 1
        if get_card_value(self.cards[this_higher_and_lower_pair_indices_tuple[0][0]], 0) < get_card_value(other_cards[other_higher_and_lower_pair_indices_tuple[0][0]], 0):
            return -1

        if get_card_value(self.cards[this_higher_and_lower_pair_indices_tuple[1][0]], 0) > get_card_value(other_cards[other_higher_and_lower_pair_indices_tuple[1][0]], 0):
            return 1
        if get_card_value(self.cards[this_higher_and_lower_pair_indices_tuple[1][0]], 0) < get_card_value(other_cards[other_higher_and_lower_pair_indices_tuple[1][0]], 0):
            return -1

        this_chosen_cards = np.take(self.cards, this_first_pair_indices)
        this_chosen_cards = np.append(this_chosen_cards, np.take(self.cards, this_second_pair_indices))
        this_reduced_cards = np.delete(self.cards, np.flatnonzero(np.isin(self.cards, this_chosen_cards)))

        other_chosen_cards = np.take(other_cards, other_first_pair_indices)
        other_chosen_cards = np.append(other_chosen_cards, np.take(other_cards, other_second_pair_indices))
        other_reduced_cards = np.delete(other_cards, np.flatnonzero(np.isin(other_cards, other_chosen_cards)))

        if get_card_value(this_reduced_cards[0], 0) > get_card_value(other_reduced_cards[0], 0):
            return 1
        if get_card_value(this_reduced_cards[0], 0) < get_card_value(other_reduced_cards[0], 0):
            return -1

        return 0
