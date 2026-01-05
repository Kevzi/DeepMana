"""Effect for Fairy Tale Slime (TOY_504t).

Card Text: <b>Battlecry:</b> Cast {0}.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Battlecry:</b> Cast {0}....
    pass