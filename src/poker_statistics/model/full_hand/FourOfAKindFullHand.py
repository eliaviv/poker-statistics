__author__ = "Eli Aviv"
__date__ = "04/11/2023"

import numpy as np

from src.poker_statistics.model.full_hand.Rank import Rank
from src.poker_statistics.model.full_hand.FullHand import FullHand
from src.poker_statistics.model.full_hand.full_hand_utils import find_high_card_index, get_card_value


class FourOfAKindFullHand(FullHand):
    def build(self, cards):
        card_vals = [card.rank.val for card in cards]
        uniques, counts = np.unique(card_vals, return_counts=True)

        if 4 not in counts:
            self.cards = None
            return

        four_of_a_kind_indices = np.where(card_vals == uniques[np.where(counts == 4)[0]])
        chosen_cards = np.take(cards, four_of_a_kind_indices)
        reduced_cards = np.delete(cards, four_of_a_kind_indices)
        chosen_cards = np.append(chosen_cards, np.take(reduced_cards, find_high_card_index(reduced_cards)))

        self.cards = list(chosen_cards)

    def rank(self):
        return Rank.FOUR_OF_A_KIND

    def compare(self, other_cards):
        this_card_vals = [card.rank.val for card in self.cards]
        this_uniques, this_counts = np.unique(this_card_vals, return_counts=True)
        this_four_of_a_kind_indices = np.where(this_card_vals == this_uniques[np.where(this_counts == 4)[0]])[0]

        other_card_vals = [card.rank.val for card in other_cards]
        other_uniques, other_counts = np.unique(other_card_vals, return_counts=True)
        other_four_of_a_kind_indices = np.where(other_card_vals == other_uniques[np.where(other_counts == 4)[0]])[0]

        if get_card_value(self.cards[this_four_of_a_kind_indices[0]], 0) > get_card_value(other_cards[other_four_of_a_kind_indices[0]], 0):
            return 1
        if get_card_value(self.cards[this_four_of_a_kind_indices[0]], 0) < get_card_value(other_cards[other_four_of_a_kind_indices[0]], 0):
            return -1

        this_reduced_cards = np.delete(self.cards, this_four_of_a_kind_indices)
        other_reduced_cards = np.delete(other_cards, other_four_of_a_kind_indices)

        if get_card_value(this_reduced_cards[0], 0) > get_card_value(other_reduced_cards[0], 0):
            return 1
        if get_card_value(this_reduced_cards[0], 0) < get_card_value(other_reduced_cards[0], 0):
            return -1

        return 0
