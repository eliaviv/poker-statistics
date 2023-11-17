__author__ = "Eli Aviv"
__date__ = "06/11/2023"

from random import randrange

from poker import Rank, Suit

from src.poker_statistics.model.full_hand.FullHandRank import FullHandRank
from src.poker_statistics.model.full_hand.StraightFlushFullHand import StraightFlushFullHand
from src.poker_statistics.model.full_hand.full_hand_utils import get_card_value, \
    find_at_least_five_ones_in_a_row, get_rank_value_val, \
    find_five_cards_in_a_row, find_high_card_index
from test.utils.test_utils import fill_with_random_cards, generate_straight_cards


def test_build_pick_straight_flush():
    # given
    suit = Suit.make_random()
    straight_flush_cards = generate_straight_cards(5, suit)
    cards = [card for card in straight_flush_cards]

    sorted_card_values = sorted([get_card_value(card, 0) for card in cards])
    if find_at_least_five_ones_in_a_row(sorted_card_values) is None:
        # only for A,2,3,4,5
        fill_with_random_cards(cards, randrange(3), excluded_ranks=[Rank('6')])
    else:
        # only for T,J,Q,K,A
        if sorted_card_values[4] == 14:
            fill_with_random_cards(cards, randrange(3), excluded_ranks=[Rank('9')])
        else:
            fill_with_random_cards(cards, randrange(3),
                                   excluded_ranks=[Rank(get_rank_value_val(sorted_card_values[0] - 1)),
                                                   Rank(get_rank_value_val(sorted_card_values[4] + 1))])

    straight_flush_full_hand = StraightFlushFullHand()

    # expected
    expected_cards = set(straight_flush_cards)

    # when
    straight_flush_full_hand.build(cards)

    # then
    assert set(straight_flush_full_hand.cards) == expected_cards


def test_build_pick_higher_straight_flush():
    # given
    suit = Suit.make_random()
    straight_flush_cards = generate_straight_cards(6, suit)
    cards = [card for card in straight_flush_cards]

    sorted_card_values = sorted([get_card_value(card, 0) for card in cards])
    indices_in_a_row = find_at_least_five_ones_in_a_row(sorted_card_values)

    if len(indices_in_a_row) != 6:
        # only for A,2,3,4,5,6
        fill_with_random_cards(cards, randrange(2), excluded_ranks=[Rank('7')])
    else:
        if sorted_card_values[5] == 14:
            fill_with_random_cards(cards, randrange(2), excluded_ranks=[Rank('8')])
        else:
            fill_with_random_cards(cards, randrange(2),
                                   excluded_ranks=[Rank(get_rank_value_val(sorted_card_values[0] - 1)),
                                                   Rank(get_rank_value_val(sorted_card_values[5] + 1))])

    straight_flush_full_hand = StraightFlushFullHand()

    # expected
    sorted_card_values = sorted([get_card_value(card, 0) for card in cards])
    if 14 in sorted_card_values and 2 in sorted_card_values and 3 in sorted_card_values:
        # only for A,2,3,4,5,...
        expected_cards = set(sorted(straight_flush_cards,
                                    key=lambda card: get_card_value(card, 1))[-5:])
    else:
        expected_cards = set(sorted(straight_flush_cards,
                                    key=lambda card: get_card_value(card, 0))[-5:])

    # when
    straight_flush_full_hand.build(cards)

    # then
    assert set(straight_flush_full_hand.cards) == expected_cards


def test_build_no_straight_flush():
    # given
    cards = []
    fill_with_random_cards(cards, randrange(5, 8), max_amount_from_random_rank=1)

    while find_five_cards_in_a_row(cards, 0) is not None:
        cards = []
        fill_with_random_cards(cards, randrange(5, 8), max_amount_from_random_rank=1)

    while find_five_cards_in_a_row(cards, 1) is not None:
        cards = []
        fill_with_random_cards(cards, randrange(5, 8), max_amount_from_random_rank=1)

    straight_flush_full_hand = StraightFlushFullHand()

    # expected
    expected_cards = None

    # when
    straight_flush_full_hand.build(cards)

    # then
    assert straight_flush_full_hand.cards == expected_cards


def test_rank():
    # expected
    expected_rank = FullHandRank.STRAIGHT_FLUSH

    # when
    straight_flush_full_hand = StraightFlushFullHand()

    # then
    assert straight_flush_full_hand.rank == expected_rank


def test_compare():
    # given
    suit = Suit.make_random()
    cards = generate_straight_cards(5, suit)

    straight_flush_full_hand = StraightFlushFullHand()
    straight_flush_full_hand.cards = cards

    other_cards = generate_straight_cards(5, suit)

    other_straight_flush_full_hand = StraightFlushFullHand()
    other_straight_flush_full_hand.cards = other_cards

    # when
    result = straight_flush_full_hand.compare(other_cards)

    # then
    value_index = 0
    sorted_card_values = sorted([get_card_value(card, 0) for card in cards])
    if find_at_least_five_ones_in_a_row(sorted_card_values) is None:
        value_index = 1
    this_high_card_index = find_high_card_index(cards, value_index)

    other_value_index = 0
    other_sorted_card_values = sorted([get_card_value(card, 0) for card in other_cards])
    if find_at_least_five_ones_in_a_row(other_sorted_card_values) is None:
        other_value_index = 1
    other_high_card_index = find_high_card_index(other_cards, other_value_index)

    if get_card_value(cards[this_high_card_index[0]], value_index) > get_card_value(other_cards[other_high_card_index[0]], other_value_index):
        assert result == 1
    elif get_card_value(cards[this_high_card_index[0]], value_index) < get_card_value(other_cards[other_high_card_index[0]], other_value_index):
        assert result == -1
    else:
        assert result == 0
