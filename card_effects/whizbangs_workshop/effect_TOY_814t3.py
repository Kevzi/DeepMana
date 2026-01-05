"""Effect for Toy Soldier (TOY_814t3).

Card Text: <b>Rush</b>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Rush</b>...
    pass