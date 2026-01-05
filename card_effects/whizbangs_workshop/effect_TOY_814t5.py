"""Effect for Toy Soldier (TOY_814t5).

Card Text: <b>Elusive</b>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Elusive</b>...
    pass