"""Effect for Power Module (TOY_330t94).

Card Text: [x]At the start of your turn,
double this minion's Attack.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]At the start of your turn,
double this minion's Attack....
    pass