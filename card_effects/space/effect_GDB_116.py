"""Effect for Eldritch Being (GDB_116).

Card Text: <b>Outcast and <b>Spellburst</b>:</b> Shuffle your hand.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Outcast and <b>Spellburst</b>:</b> Shuffle your hand....
    pass