"""Effect for Warp Gate (SC_751).

Card Text: Your next Protoss minion costs (3) less.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Your next Protoss minion costs (3) less....
    pass