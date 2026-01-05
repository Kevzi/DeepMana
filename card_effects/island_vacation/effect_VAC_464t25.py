"""Effect for Annoy-o Horn (VAC_464t25).

Card Text: Fill your board with annoying minions.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Fill your board with annoying minions....
    pass