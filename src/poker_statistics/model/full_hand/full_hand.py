__author__ = "Eli Aviv"
__date__ = "24/10/2023"

from src.poker_statistics.model.full_hand.builders.FlushBuilder import FlushBuilder
from src.poker_statistics.model.full_hand.builders.FourOfAKindBuilder import FourOfAKindBuilder
from src.poker_statistics.model.full_hand.builders.FullHouseBuilder import FullHouseBuilder
from src.poker_statistics.model.full_hand.builders.HighCardBuilder import HighCardBuilder
from src.poker_statistics.model.full_hand.builders.PairBuilder import PairBuilder
from src.poker_statistics.model.full_hand.builders.StraightBuilder import StraightBuilder
from src.poker_statistics.model.full_hand.builders.StraightFlushBuilder import StraightFlushBuilder
from src.poker_statistics.model.full_hand.builders.ThreeOfAKindBuilder import ThreeOfAKindBuilder
from src.poker_statistics.model.full_hand.builders.TwoPairBuilder import TwoPairBuilder


class FullHand:
    def __init__(self, all_cards):
        self.builder = self.build_full_hand(all_cards)

    @staticmethod
    def build_full_hand(all_cards):
        full_hand_builders = [
            StraightFlushBuilder(),
            FourOfAKindBuilder(),
            FullHouseBuilder(),
            FlushBuilder(),
            StraightBuilder(),
            ThreeOfAKindBuilder(),
            TwoPairBuilder(),
            PairBuilder(),
            HighCardBuilder()
        ]

        for builder in full_hand_builders:
            builder.build(all_cards)
            if builder.cards is not None:
                return builder

    def compare(self, other_full_hand):
        if self.builder.rank > other_full_hand.builder.rank:
            return 1

        if self.builder.rank < other_full_hand.builder.rank:
            return -1

        return self.builder.compare(other_full_hand.builder.cards)
