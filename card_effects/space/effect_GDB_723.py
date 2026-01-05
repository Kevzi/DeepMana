"""Effect for Hologram Operator (GDB_723).

Card Text: <b>Battlecry:</b> Get 3 random <b>Temporary</b> Draenei.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Battlecry:</b> Get 3 random <b>Temporary</b> Draenei....
    pass