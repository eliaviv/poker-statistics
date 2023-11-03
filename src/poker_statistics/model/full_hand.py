__author__ = "Eli Aviv"
__date__ = "24/10/2023"
__copyright__ = "Copyright (C) 2023 IXDen (https://www.ixden.com)"


class FullHand:
    def __init__(self):
        self.cards = None
        self.rank = None

    def build_full_hand(self, all_cards):
        pass


def compare_full_hands(full_hand1, full_hand2):
    if full_hand1.rank > full_hand2.rank:
        return 1

    if full_hand1.rank < full_hand2.rank:
        return -1

