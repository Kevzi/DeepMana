"""Effect for Moonkin Constellation (VAC_907t3).

Card Text: Refresh 3 Mana Crystals.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Refresh 3 Mana Crystals....
    pass