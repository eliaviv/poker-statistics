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

FULL_HAND_BUILDERS = [
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

