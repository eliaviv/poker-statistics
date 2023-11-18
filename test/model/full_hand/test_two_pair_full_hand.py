__author__ = "Eli Aviv"
__date__ = "06/11/2023"

from random import randrange

from poker import Rank

from poker_statistics.model.full_hand.FullHandRank import FullHandRank
from poker_statistics.model.full_hand.TwoPairFullHand import TwoPairFullHand
from poker_statistics.model.full_hand.full_hand_utils import get_card_value, \
    find_high_card_index, get_rank_val_value
from test.utils.test_utils import generate_same_rank_cards, fill_with_random_cards, assert_by_high_card


def test_build_pick_two_pair():
    # given
    specific_rank = Rank.make_random()
    second_specific_rank = Rank.make_random()
    while specific_rank == second_specific_rank:
        second_specific_rank = Rank.make_random()
    cards = generate_same_rank_cards([(specific_rank, 2)])
    cards.extend(generate_same_rank_cards([(second_specific_rank, 2)]))
    fill_with_random_cards(cards, randrange(1, 4), excluded_ranks=[specific_rank, second_specific_rank],
                           max_amount_from_random_rank=1)

    two_pair_full_hand = TwoPairFullHand()

    # expected
    expected_cards = {card for card in cards if card.rank == specific_rank or card.rank == second_specific_rank}
    reduced_cards = [card for card in cards if card.rank != specific_rank and card.rank != second_specific_rank]
    high_card_index = find_high_card_index(reduced_cards)[0]
    expected_cards.add(reduced_cards[high_card_index])

    # when
    two_pair_full_hand.build(cards)

    # then
    assert set(two_pair_full_hand.cards) == expected_cards


def test_build_pick_higher_two_pair():
    # given
    specific_rank = Rank.make_random()
    second_specific_rank = Rank.make_random()
    while second_specific_rank == specific_rank:
        second_specific_rank = Rank.make_random()
    third_specific_rank = Rank.make_random()
    while third_specific_rank == specific_rank or third_specific_rank == second_specific_rank:
        third_specific_rank = Rank.make_random()
    cards = generate_same_rank_cards([(specific_rank, 2)])
    cards.extend(generate_same_rank_cards([(second_specific_rank, 2)]))
    cards.extend(generate_same_rank_cards([(third_specific_rank, 2)]))
    fill_with_random_cards(cards, 1, excluded_ranks=[specific_rank, second_specific_rank, third_specific_rank])

    two_pair_full_hand = TwoPairFullHand()

    # expected
    sorted_ranks = sorted([specific_rank, second_specific_rank, third_specific_rank],
                          key=lambda rank: get_rank_val_value(rank, 0))

    expected_cards = {card for card in cards if card.rank == sorted_ranks[1] or card.rank == sorted_ranks[2]}
    reduced_cards = [card for card in cards if card.rank != sorted_ranks[1] and card.rank != sorted_ranks[2]]
    high_card_index = find_high_card_index(reduced_cards)[0]
    expected_cards.add(reduced_cards[high_card_index])

    # when
    two_pair_full_hand.build(cards)

    # then
    assert set(two_pair_full_hand.cards) == expected_cards


def test_build_no_two_pair():
    # given
    cards = []
    fill_with_random_cards(cards, randrange(5, 8), max_amount_from_random_rank=1)

    two_pair_full_hand = TwoPairFullHand()

    # expected
    expected_cards = None

    # when
    two_pair_full_hand.build(cards)

    # then
    assert two_pair_full_hand.cards == expected_cards


def test_rank():
    # expected
    expected_rank = FullHandRank.TWO_PAIR

    # when
    two_pair_full_hand = TwoPairFullHand()

    # then
    assert two_pair_full_hand.rank == expected_rank


def test_compare():
    # given
    specific_rank = Rank.make_random()
    second_specific_rank = Rank.make_random()
    while specific_rank == second_specific_rank:
        second_specific_rank = Rank.make_random()
    cards = generate_same_rank_cards([(specific_rank, 2)])
    cards.extend(generate_same_rank_cards([(second_specific_rank, 2)]))
    fill_with_random_cards(cards, 1, excluded_ranks=[specific_rank, second_specific_rank])

    two_pair_full_hand = TwoPairFullHand()
    two_pair_full_hand.cards = cards

    other_specific_rank = Rank.make_random()
    other_second_specific_rank = Rank.make_random()
    while other_specific_rank == other_second_specific_rank:
        other_second_specific_rank = Rank.make_random()
    other_cards = generate_same_rank_cards([(other_specific_rank, 2)])
    other_cards.extend(generate_same_rank_cards([(other_second_specific_rank, 2)]))
    fill_with_random_cards(other_cards, 1, excluded_ranks=[other_specific_rank, other_second_specific_rank])

    other_two_pair_full_hand = TwoPairFullHand()
    other_two_pair_full_hand.cards = other_cards

    sorted_ranks = sorted([specific_rank, second_specific_rank],
                          key=lambda rank: get_rank_val_value(rank, 0))

    other_sorted_ranks = sorted([other_specific_rank, other_second_specific_rank],
                                key=lambda rank: get_rank_val_value(rank, 0))

    higher_two_pair_cards = [card for card in cards if card.rank == sorted_ranks[1]]
    other_higher_two_pair_cards = [card for card in other_cards if card.rank == other_sorted_ranks[1]]

    # when
    result = two_pair_full_hand.compare(other_cards)

    # then
    if get_card_value(higher_two_pair_cards[0], 0) == get_card_value(other_higher_two_pair_cards[0], 0):
        lower_two_pair_cards = [card for card in cards if card.rank == sorted_ranks[0]]
        other_lower_two_pair_cards = [card for card in other_cards if card.rank == other_sorted_ranks[0]]
        if get_card_value(lower_two_pair_cards[0], 0) == get_card_value(other_lower_two_pair_cards[0], 0):
            assert_by_high_card(cards, other_cards, higher_two_pair_cards + lower_two_pair_cards, other_higher_two_pair_cards + other_lower_two_pair_cards, result)
        elif get_card_value(lower_two_pair_cards[0], 0) > get_card_value(other_lower_two_pair_cards[0], 0):
            assert result == 1
        else:
            assert result == -1
    elif get_card_value(higher_two_pair_cards[0], 0) > get_card_value(other_higher_two_pair_cards[0], 0):
        assert result == 1
    else:
        assert result == -1
