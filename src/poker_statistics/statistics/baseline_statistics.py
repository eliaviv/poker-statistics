__author__ = "Eli Aviv"
__date__ = "09/11/2023"

import multiprocessing
import statistics
from datetime import datetime

from poker import Hand

from poker_statistics.statistics.experiments.experiments import NUM_OF_GAMES_PER_EXPERIMENT

NUM_OF_EXPERIMENTS = 1000


def calculate_winning_probability_of_starting_cards(single_experiment, num_of_players):
    pool = multiprocessing.Pool()
    manager = multiprocessing.Manager()
    hands_probabilities_dict = manager.dict()

    hands = list(Hand)
    for hand in hands:
        combos = hand.to_combos()
        card1 = combos[0].first
        card2 = combos[0].second

        pool.apply_async(_run_experiments,
                         args=(single_experiment, str(hand), hands_probabilities_dict, card1.rank.val + card1.suit.val,
                               card2.rank.val + card2.suit.val, num_of_players))

    pool.close()
    pool.join()

    return _arrange_hands_probabilities(hands, hands_probabilities_dict)


def _run_experiments(single_experiment, hand_name, hands_probabilities_dict, card1_str, card2_str, num_of_players):
    print(f'{datetime.now()}: Start hand: {hand_name}')

    winning_counts = []
    for i in range(NUM_OF_EXPERIMENTS):
        winning_count = single_experiment(card1_str, card2_str, num_of_players)
        winning_counts.append(winning_count)

    average_winning_count = statistics.mean(winning_counts)
    hands_probabilities_dict[hand_name] = f'{str(round((average_winning_count / NUM_OF_GAMES_PER_EXPERIMENT) * 100, 2))}%'

    print(f'{datetime.now()}: Finish hand: {hand_name}')


def _arrange_hands_probabilities(hands, hands_probabilities_dict):
    return [f'{str(hand)}: {hands_probabilities_dict[str(hand)]}' for hand in hands]
