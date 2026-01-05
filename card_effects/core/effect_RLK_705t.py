"""Effect for Shambling Zombie (RLK_705t).

Card Text: <b>Reborn</b>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Reborn</b>...
    pass