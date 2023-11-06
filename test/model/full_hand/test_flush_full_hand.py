__author__ = "Eli Aviv"
__date__ = "06/11/2023"

from random import randrange

from poker import Suit

from src.poker_statistics.model.full_hand.FlushFullHand import FlushFullHand
from src.poker_statistics.model.full_hand.FullHandRank import FullHandRank
from src.poker_statistics.model.full_hand.full_hand_utils import CARD_VAL_TO_REAL_VALUE, get_card_value
from test.utils.test_utils import generate_same_suit_cards, fill_with_random_cards


def test_build_pick_flush():
    # given
    specific_suit = Suit.make_random()
    cards = generate_same_suit_cards(5, specific_suit)
    fill_with_random_cards(cards, randrange(3), excluded_suits=[specific_suit])

    flush_full_hand = FlushFullHand()

    # expected
    expected_cards = {card for card in cards if card.suit == specific_suit}

    # when
    flush_full_hand.build(cards)

    # then
    assert set(flush_full_hand.cards) == expected_cards


def test_build_pick_higher_flush():
    # given
    num_of_cards_of_specific_suit = 6 + randrange(2)
    specific_suit = Suit.make_random()
    cards = generate_same_suit_cards(num_of_cards_of_specific_suit, specific_suit)
    fill_with_random_cards(cards, 7 - num_of_cards_of_specific_suit, excluded_suits=[specific_suit])

    flush_full_hand = FlushFullHand()

    # expected
    chosen_cards = [card for card in cards if card.suit == specific_suit]
    expected_cards = sorted(chosen_cards, key=lambda card: CARD_VAL_TO_REAL_VALUE[card.rank.val][0])[-5:]

    # when
    flush_full_hand.build(cards)

    # then
    assert set(flush_full_hand.cards) == set(expected_cards)


def test_build_no_flush():
    # given
    num_of_cards = 5 + randrange(3)
    cards = []
    fill_with_random_cards(cards, num_of_cards, max_amount_from_random_suit=4)

    flush_full_hand = FlushFullHand()

    # expected
    expected_cards = None

    # when
    flush_full_hand.build(cards)

    # then
    assert flush_full_hand.cards == expected_cards


def test_rank():
    # expected
    expected_rank = FullHandRank.FLUSH

    # when
    flush_full_hand = FlushFullHand()

    # then
    assert flush_full_hand.rank == expected_rank


def test_compare():
    # given
    suit = Suit.make_random()
    cards = generate_same_suit_cards(5, suit)

    flush_full_hand = FlushFullHand()
    flush_full_hand.cards = cards

    other_cards = generate_same_suit_cards(5, suit)

    other_flush_full_hand = FlushFullHand()
    other_flush_full_hand.cards = other_cards

    sorted_cards = sorted(cards, key=lambda card: CARD_VAL_TO_REAL_VALUE[card.rank.val][0])
    sorted_other_cards = sorted(other_cards, key=lambda card: CARD_VAL_TO_REAL_VALUE[card.rank.val][0])

    # when
    result = flush_full_hand.compare(other_cards)

    # then
    if sorted_cards == sorted_other_cards:
        assert result == 0

    for i in range(4, 0, -1):
        if get_card_value(sorted_cards[i], 0) == get_card_value(sorted_other_cards[i], 0):
            continue
        elif get_card_value(sorted_cards[i], 0) > get_card_value(sorted_other_cards[i], 0):
            assert result == 1
            return
        else:
            assert result == -1
            return
