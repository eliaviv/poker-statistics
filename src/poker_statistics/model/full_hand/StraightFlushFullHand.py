__author__ = "Eli Aviv"
__date__ = "04/11/2023"

from poker_statistics.model.full_hand.FullHand import FullHand
from poker_statistics.model.full_hand.FullHandRank import FullHandRank
from poker_statistics.model.full_hand.full_hand_utils import find_all_cards_with_same_shape, \
    find_five_cards_in_a_row, find_high_card_index, get_card_value, find_at_least_five_ones_in_a_row


class StraightFlushFullHand(FullHand):
    def build(self, cards):
        reduced_cards = find_all_cards_with_same_shape(cards)
        if reduced_cards is None:
            self.cards = None
            return

        chosen_cards = find_five_cards_in_a_row(reduced_cards, 0)
        if chosen_cards is not None:
            self.cards = list(chosen_cards)
            return

        chosen_cards = find_five_cards_in_a_row(reduced_cards, 1)
        if chosen_cards is None:
            self.cards = None
            return

        self.cards = list(chosen_cards)

    def rank(self):
        return FullHandRank.STRAIGHT_FLUSH

    def compare(self, other_cards):
        value_index = 0
        sorted_card_values = sorted([get_card_value(card, 0) for card in self.cards])
        if find_at_least_five_ones_in_a_row(sorted_card_values) is None:
            value_index = 1
        this_high_card_index = find_high_card_index(self.cards, value_index)

        other_value_index = 0
        other_sorted_card_values = sorted([get_card_value(card, 0) for card in other_cards])
        if find_at_least_five_ones_in_a_row(other_sorted_card_values) is None:
            other_value_index = 1
        other_high_card_index = find_high_card_index(other_cards, other_value_index)

        if get_card_value(self.cards[this_high_card_index[0]], value_index) > get_card_value(other_cards[other_high_card_index[0]], other_value_index):
            return 1
        if get_card_value(self.cards[this_high_card_index[0]], value_index) < get_card_value(other_cards[other_high_card_index[0]], other_value_index):
            return -1

        return 0
