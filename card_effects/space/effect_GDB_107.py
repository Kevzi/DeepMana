"""Effect for Specimen Claw (GDB_107).

Card Text: After your opponent
plays a minion, attack it.
<b>Starship Piece</b>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: After your opponent
plays a minion, attack it.
<b>Starship Piece</b>...
    pass