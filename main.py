"""
===================================================================================
|                     N A M E  G O E S  H E R E  L O L  (v-4.4.999999)            |
|       a game made by SSS_Says_Snek#0194, aimed at upgrading snake               |
|       it's actually gonna be a terrible game, but hey, why not?                 |
|                                                                                 |
| ++-=========================================================================-++ |
|                           I N F O R M A T I O N                                 |
|                                                                                 |
|                    Date created: 4/4/2021, at 12:05 AM                          |
|                                                                                 |
===================================================================================
"""
__version__ = "-4.4.999999"
import sys

if sys.version_info < (3, 6):
    # Checks if version is below Python 3.6 (f-strings are not in Python 3.5 or below)
    print(
        """Name Goes Here Lol (Snake+) requires Python 3.6 or above to run.
          If you have problems with dependencies, or if you want support for Python 3.5 or below, submit an issue or pull request at 
          https://github.com/SSS-Says-Snek/name_goes_here_lol.""", file=sys.stderr
    )
    sys.exit(1)

from src.Engine.game import GameLoop

if __name__ == "__main__":
    # Main code to run game
    game_loop = GameLoop()
    game_loop.run()
