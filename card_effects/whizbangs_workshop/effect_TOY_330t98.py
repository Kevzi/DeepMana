"""Effect for Ticking Module (TOY_330t98).

Card Text: Costs (1) less for each friendly minion.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Costs (1) less for each friendly minion....
    pass