__author__ = "Eli Aviv"
__date__ = "01/12/2023"


from enum import Enum


class Action(Enum):
    CHECK = 0
    CALL = 1
    RAISE = 2
    FOLD = 3
