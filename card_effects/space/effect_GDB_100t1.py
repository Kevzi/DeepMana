"""Effect for Starship Pieces (GDB_100t1).

Card Text: Has the combined stats and effects of all assembled <b>Starship Pieces</b>.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Has the combined stats and effects of all assembled <b>Starship Pieces</b>....
    pass