__author__ = "Eli Aviv"
__date__ = "04/11/2023"

import numpy as np

from src.poker_statistics.model.full_hand.Rank import Rank
from src.poker_statistics.model.full_hand.builders.FullHand import FullHand
from src.poker_statistics.model.full_hand.builders.full_hand_utils import find_high_card_index, get_card_value


class HighCardFullHand(FullHand):
    def build(self, cards):
        reduced_cards = cards
        chosen_cards = np.array([])
        for i in range(0, 5):
            high_card_index = find_high_card_index(reduced_cards)
            chosen_cards = np.append(chosen_cards, np.take(reduced_cards, high_card_index))
            reduced_cards = np.delete(reduced_cards, high_card_index)

        self.cards = list(chosen_cards)

    def rank(self):
        return Rank.HIGH_CARD

    def compare(self, other_cards):
        this_reduced_cards = self.cards
        other_reduced_cards = other_cards
        for i in range(0, 5):
            this_high_card_index = find_high_card_index(this_reduced_cards)
            other_high_card_index = find_high_card_index(other_reduced_cards)

            if get_card_value(this_reduced_cards[this_high_card_index[0]], 0) > get_card_value(other_reduced_cards[other_high_card_index[0]], 0):
                return 1
            if get_card_value(this_reduced_cards[this_high_card_index[0]], 0) < get_card_value(other_reduced_cards[other_high_card_index[0]], 0):
                return -1

            this_reduced_cards = np.delete(this_reduced_cards, this_high_card_index)
            other_reduced_cards = np.delete(other_reduced_cards, other_high_card_index)

        return 0
