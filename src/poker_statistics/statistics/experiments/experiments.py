__author__ = "Eli Aviv"
__date__ = "01/12/2023"

import numpy as np
import pandas as pd
from poker import Card

from poker_statistics.model.Action import Action
from poker_statistics.model.Game import Game
from poker_statistics.model.full_hand.full_hand_utils import get_card_value

NUM_OF_GAMES_PER_EXPERIMENT = 30


def run_pre_flop_experiment(card1_str, card2_str, num_of_players):
    card1 = Card(card1_str)
    card2 = Card(card2_str)

    winning_count = 0
    for j in range(NUM_OF_GAMES_PER_EXPERIMENT):
        game = Game(num_of_players)

        game.start()

        _replace_cards_for_winning_experimented_player(game, card1, card2)

        game.deal_starting_cards()
        game.deal_rest_of_cards()
        winners = game.determine_winners()

        winner_names = [winner.name for winner in winners]
        if 'Player1' in winner_names:
            winning_count += 1

    return winning_count


def run_pre_flop_experiment_with_folds(card1_str, card2_str, num_of_players):
    num_of_folds = 4

    card1 = Card(card1_str)
    card2 = Card(card2_str)

    winning_count = 0
    for j in range(NUM_OF_GAMES_PER_EXPERIMENT):
        game = Game(num_of_players)

        game.start()

        _replace_cards_for_winning_experimented_player(game, card1, card2)
        game.deal_starting_cards()

        weakest_player_indices = _find_k_weakest_players(game.players, num_of_players, num_of_folds)
        for i in weakest_player_indices:
            game.players[i].action = Action.FOLD

        game.deal_rest_of_cards()
        winners = game.determine_winners()

        winner_names = [winner.name for winner in winners]
        if 'Player1' in winner_names:
            winning_count += 1

    return winning_count


def _replace_cards_for_winning_experimented_player(game, card1, card2):
    game.deck.remove(card1)
    game.deck.remove(card2)
    first_insert_index = len(game.deck)
    second_insert_index = len(game.deck) - len(game.players) + 1
    game.deck[first_insert_index:first_insert_index] = [card1]
    game.deck[second_insert_index:second_insert_index] = [card2]


def _find_k_weakest_players(players, num_of_players, num_of_folds, excluded_players=['Player1']):
    statistics_df = pd.read_csv(f'resources/pre_flop_statistics_{num_of_players}_players.csv', index_col=0)
    starting_hand_statistics = np.array([])
    for player in players:
        if player.name in excluded_players:
            starting_hand_statistics = np.append(starting_hand_statistics, 100.0)
            continue

        sorted_starting_hand = sorted(player.starting_hand, key=lambda card: get_card_value(card, 0))
        if sorted_starting_hand[0].suit == sorted_starting_hand[1].suit:
            starting_hand_statistics = np.append(starting_hand_statistics,
                                                 float(statistics_df[sorted_starting_hand[0].rank.val][
                                                           sorted_starting_hand[1].rank.val][:-1]))
        else:
            starting_hand_statistics = np.append(starting_hand_statistics,
                                                 float(statistics_df[sorted_starting_hand[1].rank.val][
                                                           sorted_starting_hand[0].rank.val][:-1]))

    return np.argpartition(starting_hand_statistics, num_of_folds)[:num_of_folds]
