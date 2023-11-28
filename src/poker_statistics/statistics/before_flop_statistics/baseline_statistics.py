__author__ = "Eli Aviv"
__date__ = "09/11/2023"

import multiprocessing
import statistics
from datetime import datetime

from poker import Hand, Card

from poker_statistics.model.Game import Game

NUM_OF_EXPERIMENTS = 10000
NUM_OF_GAMES_PER_EXPERIMENT = 30


def calculate_winning_probability_of_starting_cards(num_of_players):
    pool = multiprocessing.Pool()
    manager = multiprocessing.Manager()
    hands_probabilities_dict = manager.dict()

    hands = list(Hand)
    for hand in hands:
        combos = hand.to_combos()
        card1 = combos[0].first
        card2 = combos[0].second

        pool.apply_async(_run_experiments,
                         args=(str(hand), hands_probabilities_dict, card1.rank.val + card1.suit.val,
                               card2.rank.val + card2.suit.val, num_of_players))

    pool.close()
    pool.join()

    return _arrange_hands_probabilities(hands, hands_probabilities_dict)


def _run_experiments(hand_name, hands_probabilities_dict, card1_str, card2_str, num_of_players):
    print(f'{datetime.now()}: Start hand: {hand_name}')

    winning_counts, draw_counts, losing_counts = [], [], []
    for i in range(NUM_OF_EXPERIMENTS):
        winning_count, losing_count, draw_count = _run_single_experiment(card1_str, card2_str, num_of_players)

        winning_counts.append(winning_count)
        draw_counts.append(draw_count)
        losing_counts.append(losing_count)

    average_winning_count = statistics.mean(winning_counts)
    hands_probabilities_dict[hand_name] = f'{str(round((average_winning_count / NUM_OF_GAMES_PER_EXPERIMENT) * 100, 2))}%'

    print(f'{datetime.now()}: Finish hand: {hand_name}')


def _run_single_experiment(card1_str, card2_str, num_of_players):
    card1 = Card(card1_str)
    card2 = Card(card2_str)

    winning_count = 0
    draw_count = 0
    losing_count = 0
    for j in range(NUM_OF_GAMES_PER_EXPERIMENT):
        game = Game(num_of_players)

        game.start()

        game.deck.remove(card1)
        game.deck.remove(card2)

        first_insert_index = len(game.deck)
        second_insert_index = len(game.deck) - len(game.players) + 1
        game.deck[first_insert_index:first_insert_index] = [card1]
        game.deck[second_insert_index:second_insert_index] = [card2]

        game.deal_starting_cards()
        game.deal_rest_of_cards()
        winners = game.determine_winners()

        winner_names = [winner.name for winner in winners]
        if 'Player1' in winner_names:
            if len(winner_names) == 1:
                winning_count += 1
            else:
                draw_count += 1
        else:
            losing_count += 1

    return winning_count, losing_count, draw_count


def _arrange_hands_probabilities(hands, hands_probabilities_dict):
    return [f'{str(hand)}: {hands_probabilities_dict[str(hand)]}' for hand in hands]
