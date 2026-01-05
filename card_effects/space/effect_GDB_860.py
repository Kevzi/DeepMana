"""Effect for Starscale Constellar (GDB_860).

Card Text: <b><b>Spellburst</b>:</b> Double this minion's Attack.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b><b>Spellburst</b>:</b> Double this minion's Attack....
    pass