"""
===================================================================================
|                     N A M E  G O E S  H E R E  L O L  (v-5.0.0)                 |
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
__version__ = "-5.0.0"

from Engine.game import GameLoop

if __name__ == "__main__":
    game_loop = GameLoop()
    game_loop.run()
