"""Effect for Farseer Nobundo (GDB_447).

Card Text: <b>Deathrattle:</b> Open the
Galaxy's Lens. It absorbs the power of the next spell you cast.
"""

from simulator.enums import CardType

def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Deathrattle:</b> Open the
Galaxy's Lens. It absorbs the power of the next spell you cast....
    pass