"""Effect for Toy Soldier (TOY_814t).

Card Text: <b>Divine Shield</b>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Divine Shield</b>...
    pass