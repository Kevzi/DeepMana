"""Effect for Toy Soldier (TOY_814t6).

Card Text: <b>Poisonous</b>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Poisonous</b>...
    pass