__author__ = "Eli Aviv"
__date__ = "24/10/2023"

from poker_statistics.model.full_hand.FlushFullHand import FlushFullHand
from poker_statistics.model.full_hand.FourOfAKindFullHand import FourOfAKindFullHand
from poker_statistics.model.full_hand.FullHouseFullHand import FullHouseFullHand
from poker_statistics.model.full_hand.HighCardFullHand import HighCardFullHand
from poker_statistics.model.full_hand.PairFullHand import PairFullHand
from poker_statistics.model.full_hand.StraightFlushFullHand import StraightFlushFullHand
from poker_statistics.model.full_hand.StraightFullHand import StraightFullHand
from poker_statistics.model.full_hand.ThreeOfAKindFullHand import ThreeOfAKindFullHand
from poker_statistics.model.full_hand.TwoPairFullHand import TwoPairFullHand


class Player:
    def __init__(self, name):
        self.name = name
        self.starting_hand = []
        self.position = None
        self.full_hand = None
        self.action = None

    def deal_starting_hand(self, cards):
        self.starting_hand.extend(cards)

    def clear(self):
        self.starting_hand = []
        self.position = None
        self.full_hand = None

    def build_full_hand(self, cards):
        all_cards = self.starting_hand + cards

        full_hands = [
            StraightFlushFullHand(),
            FourOfAKindFullHand(),
            FullHouseFullHand(),
            FlushFullHand(),
            StraightFullHand(),
            ThreeOfAKindFullHand(),
            TwoPairFullHand(),
            PairFullHand(),
            HighCardFullHand()
        ]

        for full_hand in full_hands:
            full_hand.build(all_cards)
            if full_hand.cards is not None:
                self.full_hand = full_hand
                return

    def compare(self, other_player):
        if self.full_hand.rank > other_player.full_hand.rank:
            return 1

        if self.full_hand.rank < other_player.full_hand.rank:
            return -1

        return self.full_hand.compare(other_player.full_hand.cards)

    def __repr__(self):
        return f'{self.name} {self.position} {self.full_hand}'

    def __str__(self):
        return f'{self.name} {self.position} {self.full_hand}'
