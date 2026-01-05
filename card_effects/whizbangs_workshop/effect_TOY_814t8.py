"""Effect for Toy Soldier (TOY_814t8).

Card Text: <b>Reborn</b>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Reborn</b>...
    pass