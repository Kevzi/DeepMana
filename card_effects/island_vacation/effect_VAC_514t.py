"""Effect for Dreadhound (VAC_514t).

Card Text: <b>Reborn</b>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Reborn</b>...
    pass