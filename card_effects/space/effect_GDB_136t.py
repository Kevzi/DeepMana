"""Effect for The Galaxy's Lens (GDB_136t).

Card Text: <b><b>Spellburst</b>:</b> Absorb the spell's power!0Cast {0}.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b><b>Spellburst</b>:</b> Absorb the spell's power!0Cast {0}....
    pass