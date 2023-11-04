__author__ = "Eli Aviv"
__date__ = "04/11/2023"

from src.poker_statistics.model.full_hand.builders.FullHandBuilder import FullHandBuilder
from src.poker_statistics.model.full_hand.builders.builder_utils import find_all_cards_with_same_shape, \
    CARD_VAL_TO_REAL_VALUE


class FlushBuilder(FullHandBuilder):
    def build(self, cards):
        reduced_cards = find_all_cards_with_same_shape(cards)
        if reduced_cards is None:
            return None

        chosen_cards = sorted(reduced_cards, key=lambda card: CARD_VAL_TO_REAL_VALUE[card.rank.val][0])[-5:]

        return chosen_cards
