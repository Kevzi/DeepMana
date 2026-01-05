"""Effect for Guiding Figure (GDB_106).

Card Text: [x]<b><b>Spellburst</b>:</b> Trigger a random
friendly minion's <b>Deathrattle</b>.
<b>Starship Piece</b>
"""

from simulator.enums import CardType

def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]<b><b>Spellburst</b>:</b> Trigger a random
friendly minion's <b>Deathrattle</b>.
<b>Starship Piec...
    pass