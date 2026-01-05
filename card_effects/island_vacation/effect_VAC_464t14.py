"""Effect for Hyperblaster (VAC_464t14).

Card Text: <b>Poisonous</b>.
Your hero is <b>Immune</b> while attacking.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Poisonous</b>.
Your hero is <b>Immune</b> while attacking....
    pass