__author__ = "Eli Aviv"
__date__ = "24/10/2023"

from src.poker_statistics.statistics.before_flop_statistics import calculate_winning_probability_of_starting_cards
from src.poker_statistics.visualization.matrix_creation import save_statistics


def main():
    hands_probabilities = calculate_winning_probability_of_starting_cards()

    output_path = 'output/fre_flop_statistics_9_players.csv'
    save_statistics(hands_probabilities, output_path)


if __name__ == '__main__':
    main()
