"""Effect for Babbling Bookcase (CORE_EDR_001).

Card Text: <b>Battlecry:</b> Add 2 random Mage spells to your hand.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Battlecry:</b> Add 2 random Mage spells to your hand....
    pass