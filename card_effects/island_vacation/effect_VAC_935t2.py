"""Effect for Carry-On Suitcase (VAC_935t2).

Card Text: Get {0}.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Get {0}....
    pass