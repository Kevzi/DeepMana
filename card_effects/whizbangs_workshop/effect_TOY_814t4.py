"""Effect for Toy Soldier (TOY_814t4).

Card Text: <b>Windfury</b>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Windfury</b>...
    pass