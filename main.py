"""This is the MAIN FILE used to run the game."""
from Engine.game import GameLoop

if __name__ == "__main__":
    game_loop = GameLoop()
    game_loop.run()
