__author__ = "Eli Aviv"
__date__ = "04/11/2023"

from src.poker_statistics.model.full_hand.builders.FullHandBuilder import FullHandBuilder
from src.poker_statistics.model.full_hand.builders.builder_utils import find_five_cards_in_a_row


class StraightBuilder(FullHandBuilder):
    def build(self, cards):
        chosen_cards = find_five_cards_in_a_row(cards, 0)
        if chosen_cards is not None:
            return chosen_cards

        chosen_cards = find_five_cards_in_a_row(cards, 1)
        if chosen_cards is None:
            return None

        return chosen_cards
