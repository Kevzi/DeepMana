"""Effect for Scenic Vista (VAC_519t3).

Card Text: In 3 turns, recast every spell you played while this was in play.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: In 3 turns, recast every spell you played while this was in play....
    pass