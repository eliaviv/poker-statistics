__author__ = "Eli Aviv"
__date__ = "24/10/2023"

from src.poker_statistics.model.Game import Game


def main():
    game = Game(9)

    while True:
        game.start()


if __name__ == '__main__':
    main()
