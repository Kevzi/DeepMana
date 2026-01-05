"""Effect for Lunar Trailblazer (GDB_863).

Card Text: [x]<b>Battlecry:</b> Set the Cost of a
random spell in your hand
to this minion's Cost.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]<b>Battlecry:</b> Set the Cost of a
random spell in your hand
to this minion's Cost....
    pass