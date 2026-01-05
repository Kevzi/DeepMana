"""Effect for Crew Transport (GDB_100c).

Card Text: Get copies of all of
the <b>Starship's Pieces</b>.
Set their Costs to (1).
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Get copies of all of
the <b>Starship's Pieces</b>.
Set their Costs to (1)....
    pass