"""Effect for Magic Wisdomball (TOY_373t).

Card Text: [x]At the end of your turn,
cast a helpful Mage spell.
Lose 1 Durability.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]At the end of your turn,
cast a helpful Mage spell.
Lose 1 Durability....
    pass