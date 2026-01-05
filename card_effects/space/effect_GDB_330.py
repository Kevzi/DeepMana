"""Effect for Ur'zul Rager (GDB_330).

Card Text: <b>Lifesteal</b>
 <b><b>Spellburst</b>:</b> Attack a random enemy minion.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Lifesteal</b>
 <b><b>Spellburst</b>:</b> Attack a random enemy minion....
    pass