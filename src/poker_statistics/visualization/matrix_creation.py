__author__ = "Eli Aviv"
__date__ = "15/11/2023"

import pandas as pd

from poker_statistics.visualization import visualize


def save_statistics(hands_probabilities, num_of_players):
    statistics_matrix = [[""] * 13 for i in range(13)]

    hands_probabilities.reverse()
    for i, line in enumerate(hands_probabilities[:13]):
        split_line = line.split(": ")
        split_line[1] = split_line[1]

        statistics_matrix[i][i] = split_line[1]

    _fill_matrix(statistics_matrix, 0, hands_probabilities[13:])

    statistics_df = pd.DataFrame(statistics_matrix,
                                 index=pd.Index(['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']),
                                 columns=pd.Index(['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']))

    visualize.visualize_in_csv(statistics_df, num_of_players)
    visualize.visualize_in_html(statistics_df, num_of_players)


def _fill_matrix(matrix, i, lines):
    if len(lines) == 0:
        return

    for j in range(0, len(matrix) - i - 1):
        line = lines[2 * j]
        split_line = line.split(": ")
        split_line[1] = split_line[1]
        matrix[i][j + i + 1] = split_line[1]

        line = lines[2 * j + 1]
        split_line = line.split(": ")
        split_line[1] = split_line[1]
        matrix[j + i + 1][i] = split_line[1]

    _fill_matrix(matrix, i + 1, lines[24 - 2 * i:])


def sort_statistics():
    with open("poker_statistics/tmp_data/statistics.txt", 'r') as f:
        lines = f.readlines()

    sorted_lines = sorted(lines,
                          key=lambda line: float(line.split(': ')[1][:-2]))

    with open("poker_statistics/tmp_data/sorted_statistics.txt", 'w') as f:
        f.writelines(sorted_lines)
