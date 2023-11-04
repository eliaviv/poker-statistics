__author__ = "Eli Aviv"
__date__ = "04/11/2023"

import abc


class FullHandBuilder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def build(self, cards):
        pass
