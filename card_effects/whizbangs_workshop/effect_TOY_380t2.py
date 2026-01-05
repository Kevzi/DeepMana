"""Effect for Clay Whelp (TOY_380t2).

Card Text: <b>Elusive</b>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Elusive</b>...
    pass