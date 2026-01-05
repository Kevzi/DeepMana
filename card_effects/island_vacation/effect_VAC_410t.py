"""Effect for Angry Bird (VAC_410t).

Card Text: <b>Immune</b> while attacking.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Immune</b> while attacking....
    pass