"""Effect for Virus Module (TOY_330t96).

Card Text: <b>Elusive</b>, <b>Poisonous</b>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Elusive</b>, <b>Poisonous</b>...
    pass