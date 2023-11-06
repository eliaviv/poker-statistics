__author__ = "Eli Aviv"
__date__ = "04/11/2023"

from src.poker_statistics.model.full_hand.Rank import Rank
from src.poker_statistics.model.full_hand.FullHand import FullHand
from src.poker_statistics.model.full_hand.full_hand_utils import find_five_cards_in_a_row, find_high_card_index, \
    get_card_value


class StraightFullHand(FullHand):
    def build(self, cards):
        chosen_cards = find_five_cards_in_a_row(cards, 0)
        if chosen_cards is not None:
            self.cards = list(chosen_cards)
            return

        chosen_cards = find_five_cards_in_a_row(cards, 1)
        if chosen_cards is None:
            self.cards = None
            return

        self.cards = list(chosen_cards)

    def rank(self):
        return Rank.STRAIGHT

    def compare(self, other_cards):
        this_high_card_index = find_high_card_index(self.cards)
        other_high_card_index = find_high_card_index(other_cards)

        if get_card_value(self.cards[this_high_card_index[0]], 0) > get_card_value(other_cards[other_high_card_index[0]], 0):
            return 1
        if get_card_value(self.cards[this_high_card_index[0]], 0) < get_card_value(other_cards[other_high_card_index[0]], 0):
            return -1

        return 0