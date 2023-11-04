__author__ = "Eli Aviv"
__date__ = "04/11/2023"

import numpy as np

from src.poker_statistics.model.full_hand.builders.FullHandBuilder import FullHandBuilder
from src.poker_statistics.model.full_hand.builders.builder_utils import find_high_card_index


class HighCardBuilder(FullHandBuilder):
    def build(self, cards):
        reduced_cards = cards
        chosen_cards = np.array([])
        for i in range(0, 5):
            high_card_index = find_high_card_index(reduced_cards)
            chosen_cards = np.append(chosen_cards, np.take(reduced_cards, high_card_index))
            reduced_cards = np.delete(reduced_cards, high_card_index)

        return chosen_cards
