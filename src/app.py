__author__ = "Eli Aviv"
__date__ = "24/10/2023"

from poker_statistics.common.logging import logger
from poker_statistics.statistics.before_flop_statistics import calculate_winning_probability_of_starting_cards
from poker_statistics.visualization.matrix_creation import save_statistics

MIN_NUM_OF_PLAYERS = 2
MAX_NUM_OF_PLAYERS = 9


def main():
    logger.init_logger("Poker-Statistics")

    for i in range(MIN_NUM_OF_PLAYERS, MAX_NUM_OF_PLAYERS + 1):
        logger.log_info(f'Start calculating poker statistics for number of players: {i}')

        hands_probabilities = calculate_winning_probability_of_starting_cards(i)

        output_path = f'statistics_data/fre_flop_statistics_{i}_players.csv'
        save_statistics(hands_probabilities, output_path)


if __name__ == '__main__':
    main()
