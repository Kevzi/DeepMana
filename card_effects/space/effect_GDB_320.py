"""Effect for Eredar Brute (GDB_320).

Card Text: <b>Taunt</b>, <b>Lifesteal</b>
Costs (1) less for each enemy minion.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Taunt</b>, <b>Lifesteal</b>
Costs (1) less for each enemy minion....
    pass