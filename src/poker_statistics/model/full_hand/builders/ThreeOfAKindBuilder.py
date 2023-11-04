__author__ = "Eli Aviv"
__date__ = "04/11/2023"

import numpy as np

from src.poker_statistics.model.full_hand.builders.FullHandBuilder import FullHandBuilder
from src.poker_statistics.model.full_hand.builders.builder_utils import find_high_card_index


class ThreeOfAKindBuilder(FullHandBuilder):
    def build(self, cards):
        card_vals = [card.rank.val for card in cards]
        uniques, counts = np.unique(card_vals, return_counts=True)

        if 3 not in counts:
            return None

        three_of_a_kind_indices = np.where(card_vals == uniques[np.where(counts == 3)[0]])
        chosen_cards = np.take(cards, three_of_a_kind_indices)
        reduced_cards = np.delete(cards, three_of_a_kind_indices)

        for i in range(0, 2):
            high_card_index = find_high_card_index(reduced_cards)
            chosen_cards = np.append(chosen_cards, np.take(reduced_cards, high_card_index))
            reduced_cards = np.delete(reduced_cards, high_card_index)

        return chosen_cards
