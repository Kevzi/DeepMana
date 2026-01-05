"""Effect for Zealot (SC_751t).

Card Text: <b>Charge</b>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Charge</b>...
    pass