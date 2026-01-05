"""Effect for Carry-On Suitcase (VAC_935t).

Card Text: Get {0} and {1}.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Get {0} and {1}....
    pass