__author__ = "Eli Aviv"
__date__ = "06/11/2023"

from random import randrange

from poker import Rank

from src.poker_statistics.model.full_hand.FullHandRank import FullHandRank
from src.poker_statistics.model.full_hand.PairFullHand import PairFullHand
from src.poker_statistics.model.full_hand.full_hand_utils import get_card_value, \
    find_high_card_index
from test.utils.test_utils import generate_same_rank_cards, fill_with_random_cards, assert_by_high_card


def test_build_pick_pair():
    # given
    specific_rank = Rank.make_random()
    cards = generate_same_rank_cards([(specific_rank, 2)])
    fill_with_random_cards(cards, randrange(3, 6), excluded_ranks=[specific_rank], max_amount_from_random_rank=1)

    pair_full_hand = PairFullHand()

    # expected
    expected_cards = {card for card in cards if card.rank == specific_rank}
    reduced_cards = [card for card in cards if card.rank != specific_rank]
    for i in range(3):
        high_card_index = find_high_card_index(reduced_cards)[0]
        expected_cards.add(reduced_cards[high_card_index])
        reduced_cards.remove(reduced_cards[high_card_index])

    # when
    pair_full_hand.build(cards)

    # then
    assert set(pair_full_hand.cards) == expected_cards


def test_build_no_pair():
    # given
    cards = []
    fill_with_random_cards(cards, randrange(5, 8), max_amount_from_random_rank=1)

    pair_full_hand = PairFullHand()

    # expected
    expected_cards = None

    # when
    pair_full_hand.build(cards)

    # then
    assert pair_full_hand.cards == expected_cards


def test_rank():
    # expected
    expected_rank = FullHandRank.PAIR

    # when
    pair_full_hand = PairFullHand()

    # then
    assert pair_full_hand.rank == expected_rank


def test_compare():
    # given
    specific_rank = Rank.make_random()
    cards = generate_same_rank_cards([(specific_rank, 2)])
    fill_with_random_cards(cards, 3, excluded_ranks=[specific_rank], max_amount_from_random_rank=1)

    pair_full_hand = PairFullHand()
    pair_full_hand.cards = cards

    other_specific_rank = Rank.make_random()
    other_cards = generate_same_rank_cards([(other_specific_rank, 2)])
    fill_with_random_cards(other_cards, 3, excluded_ranks=[other_specific_rank], max_amount_from_random_rank=1)

    other_pair_full_hand = PairFullHand()
    other_pair_full_hand.cards = other_cards

    pair_cards = [card for card in cards if card.rank == specific_rank]
    other_pair_cards = [card for card in other_cards if card.rank == other_specific_rank]

    # when
    result = pair_full_hand.compare(other_cards)

    # then
    if get_card_value(pair_cards[0], 0) == get_card_value(other_pair_cards[0], 0):
        assert_by_high_card(cards, other_cards, pair_cards, other_pair_cards, result)
    elif get_card_value(pair_cards[0], 0) > get_card_value(other_pair_cards[0], 0):
        assert result == 1
    else:
        assert result == -1

