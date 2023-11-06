__author__ = "Eli Aviv"
__date__ = "04/11/2023"

import abc


class FullHand(metaclass=abc.ABCMeta):
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

    def __repr__(self):
        return f'{self.rank} {self.cards}'

    def __str__(self):
        return f'{self.rank} {self.cards}'
