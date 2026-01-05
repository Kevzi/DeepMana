"""Effect for Supernova (GDB_301).

Card Text: Fill your hand with random Fire spells. They cost (1).
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Fill your hand with random Fire spells. They cost (1)....
    pass