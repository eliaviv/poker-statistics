__author__ = "Eli Aviv"
__date__ = "04/11/2023"

import abc

from src.poker_statistics.model.full_hand.builders.builder_utils import find_high_card_index


class FullHandBuilder(metaclass=abc.ABCMeta):
    def __init__(self):
        self.rank = self.rank()
        self.cards = None

    @abc.abstractmethod
    def build(self, cards):
        pass

    @abc.abstractmethod
    def rank(self):
        pass

    @abc.abstractmethod
    def compare(self, other_cards):
        pass
