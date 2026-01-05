"""Effect for Exarch Othaar (GDB_856).

Card Text: [x]<b>Battlecry:</b> If you're building
a <b>Starship</b>, get 3 different
Arcane spells and reduce
their Costs by (2).
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]<b>Battlecry:</b> If you're building
a <b>Starship</b>, get 3 different
Arcane spells and reduce
...
    pass