__author__ = "Eli Aviv"
__date__ = "09/11/2023"

import statistics

from poker import Hand

from poker_statistics.model.Game import Game

NUM_OF_EXPERIMENTS = 1000
NUM_OF_GAMES_PER_EXPERIMENT = 30


def calculate_winning_probability_of_starting_cards(num_of_players):
    hands = list(Hand)
    hands_probabilities = []
    for hand in hands:
        combos = hand.to_combos()
        card1 = combos[0].first
        card2 = combos[0].second

        winning_counts = []
        draw_counts = []
        losing_counts = []
        for i in range(NUM_OF_EXPERIMENTS):
            winning_count, losing_count, draw_count = _run_experiment(card1, card2, num_of_players)

            winning_counts.append(winning_count)
            draw_counts.append(draw_count)
            losing_counts.append(losing_count)

        average_winning_count = statistics.mean(winning_counts)
        hands_probabilities.append(f'{str(hand)}: {str(round((average_winning_count / 30) * 100, 2))}%')

    return hands_probabilities


def _run_experiment(card1, card2, num_of_players):
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
