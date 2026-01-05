"""Effect for Horn of Winter (CORE_RLK_042).

Card Text: Refresh 2 Mana Crystals.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Refresh 2 Mana Crystals....
    pass