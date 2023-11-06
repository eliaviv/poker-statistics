__author__ = "Eli Aviv"
__date__ = "04/11/2023"

import numpy as np

from src.poker_statistics.model.full_hand.FullHand import FullHand
from src.poker_statistics.model.full_hand.FullHandRank import FullHandRank
from src.poker_statistics.model.full_hand.full_hand_utils import find_high_card_index, get_card_value


class PairFullHand(FullHand):
    def build(self, cards):
        card_vals = [card.rank.val for card in cards]
        uniques, counts = np.unique(card_vals, return_counts=True)

        if 2 not in counts:
            self.cards = None
            return

        pair_indices = np.where(card_vals == uniques[np.where(counts == 2)[0]])
        chosen_cards = np.take(cards, pair_indices)
        reduced_cards = np.delete(cards, pair_indices)

        for i in range(0, 3):
            high_card_index = find_high_card_index(reduced_cards)
            chosen_cards = np.append(chosen_cards, np.take(reduced_cards, high_card_index))
            reduced_cards = np.delete(reduced_cards, high_card_index)

        self.cards = list(chosen_cards)

    def rank(self):
        return FullHandRank.PAIR

    def compare(self, other_cards):
        this_card_vals = [card.rank.val for card in self.cards]
        this_uniques, this_counts = np.unique(this_card_vals, return_counts=True)
        this_pair_indices = np.where(this_card_vals == this_uniques[np.where(this_counts == 2)[0]])[0]

        other_card_vals = [card.rank.val for card in other_cards]
        other_uniques, other_counts = np.unique(other_card_vals, return_counts=True)
        other_pair_indices = np.where(other_card_vals == other_uniques[np.where(other_counts == 2)[0]])[0]

        if get_card_value(self.cards[this_pair_indices[0]], 0) > get_card_value(other_cards[other_pair_indices[0]], 0):
            return 1
        if get_card_value(self.cards[this_pair_indices[0]], 0) < get_card_value(other_cards[other_pair_indices[0]], 0):
            return -1

        this_reduced_cards = np.delete(self.cards, this_pair_indices)
        other_reduced_cards = np.delete(other_cards, other_pair_indices)

        for i in range(0, 3):
            this_high_card_index = find_high_card_index(this_reduced_cards)
            other_high_card_index = find_high_card_index(other_reduced_cards)

            if get_card_value(this_reduced_cards[this_high_card_index[0]], 0) > get_card_value(other_reduced_cards[other_high_card_index[0]], 0):
                return 1
            if get_card_value(this_reduced_cards[this_high_card_index[0]], 0) < get_card_value(other_reduced_cards[other_high_card_index[0]], 0):
                return -1

            this_reduced_cards = np.delete(this_reduced_cards, this_high_card_index)
            other_reduced_cards = np.delete(other_reduced_cards, other_high_card_index)

        return 0
