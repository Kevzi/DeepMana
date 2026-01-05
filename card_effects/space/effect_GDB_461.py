"""Effect for Astral Vigilant (GDB_461).

Card Text: <b>Battlecry:</b> Get a copy of the last Draenei you played.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Battlecry:</b> Get a copy of the last Draenei you played....
    pass