__author__ = "Eli Aviv"
__date__ = "06/11/2023"

from random import randrange

from poker import Rank

from poker_statistics.model.full_hand.FourOfAKindFullHand import FourOfAKindFullHand
from poker_statistics.model.full_hand.FullHandRank import FullHandRank
from poker_statistics.model.full_hand.full_hand_utils import get_card_value, \
    find_high_card_index
from test.utils.test_utils import generate_same_rank_cards, fill_with_random_cards


def test_build_pick_four_of_a_kind():
    # given
    specific_rank = Rank.make_random()
    cards = generate_same_rank_cards([(specific_rank, 4)])
    fill_with_random_cards(cards, randrange(1, 4), excluded_ranks=[specific_rank])

    four_of_a_kind_full_hand = FourOfAKindFullHand()

    # expected
    expected_cards = {card for card in cards if card.rank == specific_rank}
    reduced_cards = [card for card in cards if card.rank != specific_rank]
    high_card_index = find_high_card_index(reduced_cards)[0]
    expected_cards.add(reduced_cards[high_card_index])

    # when
    four_of_a_kind_full_hand.build(cards)

    # then
    assert set(four_of_a_kind_full_hand.cards) == expected_cards


def test_build_no_four_of_a_kind():
    # given
    cards = []
    fill_with_random_cards(cards, randrange(5, 8), max_amount_from_random_rank=3)

    four_of_a_kind_full_hand = FourOfAKindFullHand()

    # expected
    expected_cards = None

    # when
    four_of_a_kind_full_hand.build(cards)

    # then
    assert four_of_a_kind_full_hand.cards == expected_cards


def test_rank():
    # expected
    expected_rank = FullHandRank.FOUR_OF_A_KIND

    # when
    four_of_a_kind_full_hand = FourOfAKindFullHand()

    # then
    assert four_of_a_kind_full_hand.rank == expected_rank


def test_compare():
    # given
    specific_rank = Rank.make_random()
    cards = generate_same_rank_cards([(specific_rank, 4)])
    fill_with_random_cards(cards, 1, excluded_ranks=[specific_rank])

    four_of_a_kind_full_hand = FourOfAKindFullHand()
    four_of_a_kind_full_hand.cards = cards

    other_specific_rank = Rank.make_random()
    other_cards = generate_same_rank_cards([(other_specific_rank, 4)])
    fill_with_random_cards(other_cards, 1, excluded_ranks=[other_specific_rank])

    other_four_of_a_kind_full_hand = FourOfAKindFullHand()
    other_four_of_a_kind_full_hand.cards = other_cards

    card_value_to_compare = get_card_value([card for card in cards if card.rank == specific_rank][0], 0)
    other_card_value_to_compare = get_card_value([card for card in other_cards if card.rank == other_specific_rank][0], 0)

    # when
    result = four_of_a_kind_full_hand.compare(other_cards)

    # then
    if card_value_to_compare == other_card_value_to_compare:
        card_value_to_compare = get_card_value([card for card in cards if card.rank != specific_rank][0], 0)
        other_card_value_to_compare = get_card_value([card for card in other_cards if card.rank != specific_rank][0], 0)
        if card_value_to_compare == other_card_value_to_compare:
            assert result == 0
        elif card_value_to_compare > other_card_value_to_compare:
            assert result == 1
        else:
            assert result == -1
    elif card_value_to_compare > other_card_value_to_compare:
        assert result == 1
    else:
        assert result == -1
