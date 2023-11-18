__author__ = "Eli Aviv"
__date__ = "24/10/2023"

from poker_statistics.common.logging import logger
from poker_statistics.statistics.before_flop_statistics import calculate_winning_probability_of_starting_cards
from poker_statistics.visualization.matrix_creation import save_statistics

MIN_NUM_OF_PLAYERS = 2
MAX_NUM_OF_PLAYERS = 9


def main():
    logger.init_logger("Poker-Statistics")

    _calculate_pre_flop_statistics()


def _calculate_pre_flop_statistics():
    for i in range(MAX_NUM_OF_PLAYERS, MIN_NUM_OF_PLAYERS - 1, -1):
        logger.log_info(f'\nStart calculating poker statistics for number of players: {i}\n')

        hands_probabilities = calculate_winning_probability_of_starting_cards(i)

        output_path = f'statistics_data/fre_flop_statistics_{i}_players.csv'
        save_statistics(hands_probabilities, output_path)


if __name__ == '__main__':
    main()
