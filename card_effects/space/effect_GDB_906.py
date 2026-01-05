"""Effect for Abort Launch (GDB_906).

Card Text: Abort Launch.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Abort Launch....
    pass