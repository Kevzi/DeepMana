"""Effect for Scrounging Shipwright (GDB_876).

Card Text: <b>Battlecry:</b> Get a random <b>Starship Piece</b> from another class.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Battlecry:</b> Get a random <b>Starship Piece</b> from another class....
    pass