__author__ = "Eli Aviv"
__date__ = "24/10/2023"

from datetime import datetime

from poker_statistics.statistics.baseline_statistics import \
    calculate_winning_probability_of_starting_cards
from poker_statistics.statistics.experiments.experiments import run_pre_flop_experiment, \
    run_pre_flop_experiment_with_folds
from poker_statistics.visualization.matrix_creation import save_statistics

MIN_NUM_OF_PLAYERS = 2
MAX_NUM_OF_PLAYERS = 9


def main():
    _calculate_pre_flop_statistics(run_pre_flop_experiment_with_folds)


def _calculate_pre_flop_statistics(single_experiment):
    for i in range(MAX_NUM_OF_PLAYERS, MIN_NUM_OF_PLAYERS - 1, -1):
        print(f'\n{datetime.now()}: Start calculating poker statistics for number of players: {i}\n')

        hands_probabilities = calculate_winning_probability_of_starting_cards(single_experiment, i)

        save_statistics(hands_probabilities, i)


if __name__ == '__main__':
    main()
