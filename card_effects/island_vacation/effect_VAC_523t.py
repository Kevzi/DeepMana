"""Effect for Mixologist's Special (VAC_523t).

Card Text: {0}
{1}
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: {0}
{1}...
    pass