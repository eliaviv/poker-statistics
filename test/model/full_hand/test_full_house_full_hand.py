__author__ = "Eli Aviv"
__date__ = "06/11/2023"

from random import randrange

import numpy as np
from poker import Rank

from poker_statistics.model.full_hand.FullHandRank import FullHandRank
from poker_statistics.model.full_hand.FullHouseFullHand import FullHouseFullHand
from poker_statistics.model.full_hand.full_hand_utils import get_card_value, \
    CARD_VAL_TO_REAL_VALUE
from test.utils.test_utils import generate_same_rank_cards, fill_with_random_cards


def test_build_pick_full_house():
    # given
    specific_rank = Rank.make_random()
    second_specific_rank = Rank.make_random()
    while second_specific_rank == specific_rank:
        second_specific_rank = Rank.make_random()
    cards = generate_same_rank_cards([(specific_rank, 3), (second_specific_rank, 2)])
    fill_with_random_cards(cards, randrange(3), excluded_ranks=[specific_rank, second_specific_rank], max_amount_from_random_rank=1)

    full_house_full_hand = FullHouseFullHand()

    # expected
    expected_cards = {card for card in cards if card.rank == specific_rank}
    expected_cards.update({card for card in cards if card.rank == second_specific_rank})

    # when
    full_house_full_hand.build(cards)

    # then
    assert set(full_house_full_hand.cards) == expected_cards


def test_build_pick_higher_full_house():
    # given
    specific_rank = Rank.make_random()
    second_specific_rank = Rank.make_random()
    while second_specific_rank == specific_rank:
        second_specific_rank = Rank.make_random()
    cards = generate_same_rank_cards([(specific_rank, 3), (second_specific_rank, 3)])
    fill_with_random_cards(cards, randrange(2), excluded_ranks=[specific_rank, second_specific_rank])

    full_house_full_hand = FullHouseFullHand()

    # expected
    expected_cards = dict()
    if CARD_VAL_TO_REAL_VALUE[specific_rank.val][0] > CARD_VAL_TO_REAL_VALUE[second_specific_rank.val][0]:
        expected_cards[specific_rank] = 3
        expected_cards[second_specific_rank] = 2
    else:
        expected_cards[specific_rank] = 2
        expected_cards[second_specific_rank] = 3

    # when
    full_house_full_hand.build(cards)

    # then
    card_ranks = [card.rank for card in full_house_full_hand.cards]
    uniques, counts = np.unique(card_ranks, return_counts=True)
    uniques_dict = dict(zip(uniques, counts))
    assert uniques_dict == expected_cards


def test_build_pick_higher_full_house_2():
    # given
    specific_rank = Rank.make_random()
    second_specific_rank = Rank.make_random()
    while second_specific_rank == specific_rank:
        second_specific_rank = Rank.make_random()
    third_specific_rank = Rank.make_random()
    while third_specific_rank == specific_rank or third_specific_rank == second_specific_rank:
        third_specific_rank = Rank.make_random()
    cards = generate_same_rank_cards([(specific_rank, 3), (second_specific_rank, 2), (third_specific_rank, 2)])

    full_house_full_hand = FullHouseFullHand()

    # expected
    expected_cards = dict()
    expected_cards[specific_rank] = 3
    if CARD_VAL_TO_REAL_VALUE[second_specific_rank.val][0] > CARD_VAL_TO_REAL_VALUE[third_specific_rank.val][0]:
        expected_cards[second_specific_rank] = 2
    else:
        expected_cards[third_specific_rank] = 2

    # when
    full_house_full_hand.build(cards)

    # then
    card_ranks = [card.rank for card in full_house_full_hand.cards]
    uniques, counts = np.unique(card_ranks, return_counts=True)
    uniques_dict = dict(zip(uniques, counts))
    assert uniques_dict == expected_cards


def test_build_no_full_house():
    # given
    cards = []
    fill_with_random_cards(cards, randrange(5, 8), max_amount_from_random_rank=randrange(1, 3))

    full_house_full_hand = FullHouseFullHand()

    # expected
    expected_cards = None

    # when
    full_house_full_hand.build(cards)

    # then
    assert full_house_full_hand.cards == expected_cards


def test_rank():
    # expected
    expected_rank = FullHandRank.FULL_HOUSE

    # when
    full_house_full_hand = FullHouseFullHand()

    # then
    assert full_house_full_hand.rank == expected_rank


def test_compare():
    # given
    specific_rank = Rank.make_random()
    second_specific_rank = Rank.make_random()
    while second_specific_rank == specific_rank:
        second_specific_rank = Rank.make_random()
    cards = generate_same_rank_cards([(specific_rank, 3), (second_specific_rank, 2)])

    full_house_full_hand = FullHouseFullHand()
    full_house_full_hand.cards = cards

    other_specific_rank = Rank.make_random()
    second_other_specific_rank = Rank.make_random()
    while second_other_specific_rank == other_specific_rank:
        second_other_specific_rank = Rank.make_random()
    other_cards = generate_same_rank_cards([(other_specific_rank, 3), (second_other_specific_rank, 2)])

    other_full_house_full_hand = FullHouseFullHand()
    other_full_house_full_hand.cards = other_cards

    reduced_cards = [card for card in cards if card.rank == specific_rank]
    card_to_compare = reduced_cards[0]
    reduced_other_cards = [card for card in other_cards if card.rank == other_specific_rank]
    other_card_to_compare = reduced_other_cards[0]

    # when
    result = full_house_full_hand.compare(other_cards)

    # then
    if get_card_value(card_to_compare, 0) == get_card_value(other_card_to_compare, 0):
        reduced_cards = [card for card in cards if card.rank == second_specific_rank]
        card_to_compare = reduced_cards[0]
        reduced_other_cards = [card for card in other_cards if card.rank == second_other_specific_rank]
        other_card_to_compare = reduced_other_cards[0]
        if get_card_value(card_to_compare, 0) == get_card_value(other_card_to_compare, 0):
            assert result == 0
        elif get_card_value(card_to_compare, 0) > get_card_value(other_card_to_compare, 0):
            assert result == 1
        else:
            assert result == -1
    elif get_card_value(card_to_compare, 0) > get_card_value(other_card_to_compare, 0):
        assert result == 1
    else:
        assert result == -1
