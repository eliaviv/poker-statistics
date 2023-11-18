__author__ = "Eli Aviv"
__date__ = "06/11/2023"

from random import randrange

from poker_statistics.model.full_hand.FullHandRank import FullHandRank
from poker_statistics.model.full_hand.HighCardFullHand import HighCardFullHand
from poker_statistics.model.full_hand.full_hand_utils import find_high_card_index
from test.utils.test_utils import fill_with_random_cards, assert_by_high_card


def test_build_pick_high_card():
    # given
    cards = []
    fill_with_random_cards(cards, randrange(5, 8), max_amount_from_random_rank=1)

    high_card_full_hand = HighCardFullHand()

    # expected
    expected_cards = set()
    reduced_cards = [card for card in cards]
    for i in range(5):
        high_card_index = find_high_card_index(reduced_cards)[0]
        expected_cards.add(reduced_cards[high_card_index])
        reduced_cards.remove(reduced_cards[high_card_index])

    # when
    high_card_full_hand.build(cards)

    # then
    assert set(high_card_full_hand.cards) == expected_cards


def test_rank():
    # expected
    expected_rank = FullHandRank.HIGH_CARD

    # when
    high_card_full_hand = HighCardFullHand()

    # then
    assert high_card_full_hand.rank == expected_rank


def test_compare():
    # given
    cards = []
    fill_with_random_cards(cards, 5, max_amount_from_random_rank=1)

    high_card_full_hand = HighCardFullHand()
    high_card_full_hand.cards = cards

    other_cards = []
    fill_with_random_cards(other_cards, 5, max_amount_from_random_rank=1)

    other_high_card_full_hand = HighCardFullHand()
    other_high_card_full_hand.cards = other_cards

    # when
    result = high_card_full_hand.compare(other_cards)

    # then
    assert_by_high_card(cards, other_cards, [], [], result)
