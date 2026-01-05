"""Effect for Lumia (GDB_144).

Card Text: [x]<b>Lifesteal</b>
After a hero takes damage,
they become <b>Immune</b> for
the rest of the turn.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]<b>Lifesteal</b>
After a hero takes damage,
they become <b>Immune</b> for
the rest of the turn....
    pass