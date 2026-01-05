"""Effect for SCV (SC_401).

Card Text: <b>Battlecry:</b> Your next <b>Starship</b> launch costs
(2) less.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Battlecry:</b> Your next <b>Starship</b> launch costs
(2) less....
    pass