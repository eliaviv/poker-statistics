__author__ = "Eli Aviv"
__date__ = "05/11/2023"

import random

from poker import Card

from src.poker_statistics.model.Player import Player


class Game:
    def __init__(self, num_of_players):
        self.deck = None
        self.players = self.create_players(num_of_players)
        self.small_blind_position = 0
        self.game_number = 1

    def start(self):
        print(f'Game #{self.game_number} Started')

        self.set_positions()

        self.deck = list(Card)
        random.shuffle(self.deck)

        self.deal_starting_cards()
        self.deal_rest_of_cards()
        winners = self.determine_winner()

        print(f'Winners: {winners}\n')

        self.prepare_for_next_round()

        self.game_number += 1

    def deal_starting_cards(self):
        for i in range(2):
            next_player_index = self.small_blind_position
            for j in range(len(self.players)):
                starting_card = [self.deck.pop()]
                self.players[next_player_index % len(self.players)].deal_starting_hand(starting_card)
                next_player_index += 1

        for player in self.players:
            print(f'{player.name} starting hand: {player.starting_hand}')
        print()

    def deal_rest_of_cards(self):
        all_cards = []

        self.deck.pop()
        flop = [self.deck.pop() for __ in range(3)]
        print(f'Flop: {flop}')
        all_cards.extend(flop)
        for player in self.players:
            player.build_full_hand(all_cards)

        self.deck.pop()
        turn = [self.deck.pop()]
        print(f'Turn: {turn}')
        all_cards.extend(turn)
        for player in self.players:
            player.build_full_hand(all_cards)

        self.deck.pop()
        river = [self.deck.pop()]
        print(f'River: {river}\n')
        all_cards.extend(river)
        for player in self.players:
            player.build_full_hand(all_cards)

    def determine_winner(self):
        players_with_best_hand = [self.players[0]]
        for i in range(1, len(self.players)):
            result = players_with_best_hand[0].compare(self.players[i])
            if result == 0:
                players_with_best_hand.append(self.players[i])
            elif result == -1:
                players_with_best_hand.clear()
                players_with_best_hand.append(self.players[i])

        return players_with_best_hand

    def prepare_for_next_round(self):
        self.small_blind_position = (self.small_blind_position + 1) % len(self.players)
        for player in self.players:
            player.clear()

    def set_positions(self):
        next_player_index = self.small_blind_position
        for i in range(len(self.players)):
            positions = NUM_OF_PLAYERS_TO_POSITIONS[len(self.players)]
            self.players[next_player_index % len(self.players)].position = positions[i]
            next_player_index += 1

    @staticmethod
    def create_players(num_of_players):
        return [Player(f'Player{i}') for i in range(1, num_of_players + 1)]


POSITIONS_9_PLAYERS = [
    'SMALL BLIND',
    'BIG BLIND',
    'UNDER THE GUN',
    'UNDER THE GUN + 1',
    'MIDDLE POSITION',
    'LOJACK',
    'HIJACK',
    'CUT OFF',
    'BUTTON',
]

NUM_OF_PLAYERS_TO_POSITIONS = {
    9: POSITIONS_9_PLAYERS
}
