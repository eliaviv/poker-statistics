__author__ = "Eli Aviv"
__date__ = "06/11/2023"

from random import randrange

from poker import Rank

from poker_statistics.model.full_hand.FullHandRank import FullHandRank
from poker_statistics.model.full_hand.ThreeOfAKindFullHand import ThreeOfAKindFullHand
from poker_statistics.model.full_hand.full_hand_utils import get_card_value, \
    find_high_card_index
from test.utils.test_utils import generate_same_rank_cards, fill_with_random_cards, assert_by_high_card


def test_build_pick_three_of_a_kind():
    # given
    specific_rank = Rank.make_random()
    cards = generate_same_rank_cards([(specific_rank, 3)])
    fill_with_random_cards(cards, randrange(2, 5), excluded_ranks=[specific_rank], max_amount_from_random_rank=1)

    three_of_a_kind_full_hand = ThreeOfAKindFullHand()

    # expected
    expected_cards = {card for card in cards if card.rank == specific_rank}
    reduced_cards = [card for card in cards if card.rank != specific_rank]
    high_card_index = find_high_card_index(reduced_cards)[0]
    expected_cards.add(reduced_cards[high_card_index])
    reduced_cards.remove(reduced_cards[high_card_index])
    high_card_index = find_high_card_index(reduced_cards)[0]
    expected_cards.add(reduced_cards[high_card_index])

    # when
    three_of_a_kind_full_hand.build(cards)

    # then
    assert set(three_of_a_kind_full_hand.cards) == expected_cards


def test_build_no_three_of_a_kind():
    # given
    cards = []
    fill_with_random_cards(cards, randrange(5, 8), max_amount_from_random_rank=2)

    three_of_a_kind_full_hand = ThreeOfAKindFullHand()

    # expected
    expected_cards = None

    # when
    three_of_a_kind_full_hand.build(cards)

    # then
    assert three_of_a_kind_full_hand.cards == expected_cards


def test_rank():
    # expected
    expected_rank = FullHandRank.THREE_OF_A_KIND

    # when
    three_of_a_kind_full_hand = ThreeOfAKindFullHand()

    # then
    assert three_of_a_kind_full_hand.rank == expected_rank


def test_compare():
    # given
    specific_rank = Rank.make_random()
    cards = generate_same_rank_cards([(specific_rank, 3)])
    fill_with_random_cards(cards, 2, excluded_ranks=[specific_rank], max_amount_from_random_rank=1)

    three_of_a_kind_full_hand = ThreeOfAKindFullHand()
    three_of_a_kind_full_hand.cards = cards

    other_specific_rank = Rank.make_random()
    other_cards = generate_same_rank_cards([(other_specific_rank, 3)])
    fill_with_random_cards(other_cards, 2, excluded_ranks=[other_specific_rank], max_amount_from_random_rank=1)

    other_three_of_a_kind_full_hand = ThreeOfAKindFullHand()
    other_three_of_a_kind_full_hand.cards = other_cards

    three_of_a_kind_cards = [card for card in cards if card.rank == specific_rank]
    other_three_of_a_kind_cards = [card for card in other_cards if card.rank == other_specific_rank]

    # when
    result = three_of_a_kind_full_hand.compare(other_cards)

    # then
    if get_card_value(three_of_a_kind_cards[0], 0) == get_card_value(other_three_of_a_kind_cards[0], 0):
        assert_by_high_card(cards, other_cards, three_of_a_kind_cards, other_three_of_a_kind_cards, result)
    elif get_card_value(three_of_a_kind_cards[0], 0) > get_card_value(other_three_of_a_kind_cards[0], 0):
        assert result == 1
    else:
        assert result == -1
