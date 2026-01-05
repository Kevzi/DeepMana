"""Effect for Toy Soldier (TOY_814t7).

Card Text: <b>Lifesteal</b>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Lifesteal</b>...
    pass