"""Effect for Starlight Reactor (GDB_108).

Card Text: After you cast an Arcane spell, recast it <i>(targets chosen randomly)</i>.
<b>Starship Piece</b>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: After you cast an Arcane spell, recast it <i>(targets chosen randomly)</i>.
<b>Starship Piece</b>...
    pass