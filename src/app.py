__author__ = "Eli Aviv"
__date__ = "24/10/2023"

from datetime import datetime

from poker_statistics.statistics.before_flop_statistics.baseline_statistics import \
    calculate_winning_probability_of_starting_cards
from poker_statistics.visualization.matrix_creation import save_statistics

MIN_NUM_OF_PLAYERS = 2
MAX_NUM_OF_PLAYERS = 9


def main():
    # logger.init_logger("Poker-Statistics")

    _calculate_pre_flop_statistics()
    # _calculate_pre_flop_statistics_when_half_folds()


def _calculate_pre_flop_statistics():
    for i in range(MAX_NUM_OF_PLAYERS, MIN_NUM_OF_PLAYERS - 1, -1):
        print(f'\n{datetime.now()}: Start calculating poker statistics for number of players: {i}\n')

        hands_probabilities = calculate_winning_probability_of_starting_cards(i)

        save_statistics(hands_probabilities, i)


if __name__ == '__main__':
    main()
