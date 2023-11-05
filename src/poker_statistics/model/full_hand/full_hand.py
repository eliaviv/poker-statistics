__author__ = "Eli Aviv"
__date__ = "24/10/2023"

from src.poker_statistics.model.full_hand.builders.FlushFullHand import FlushFullHand
from src.poker_statistics.model.full_hand.builders.FourOfAKindFullHand import FourOfAKindFullHand
from src.poker_statistics.model.full_hand.builders.FullHouseFullHand import FullHouseFullHand
from src.poker_statistics.model.full_hand.builders.HighCardFullHand import HighCardFullHand
from src.poker_statistics.model.full_hand.builders.PairFullHand import PairFullHand
from src.poker_statistics.model.full_hand.builders.StraightFullHand import StraightFullHand
from src.poker_statistics.model.full_hand.builders.StraightFlushFullHand import StraightFlushFullHand
from src.poker_statistics.model.full_hand.builders.ThreeOfAKindFullHand import ThreeOfAKindFullHand
from src.poker_statistics.model.full_hand.builders.TwoPairFullHand import TwoPairFullHand


class Player:
    def __init__(self):
        self.starting_hand = None
        self.full_hand = None

    def deal_starting_hand(self, cards):
        self.starting_hand = cards

    def build_full_hand(self, cards):
        if self.full_hand is None:
            all_cards = self.starting_hand + cards
        else:
            all_cards = self.full_hand.cards + cards

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
