"""Effect for Nexus-Prince Shaffar (GDB_143).

Card Text: [x]<b>Spellburst:</b> Give a minion
in your hand +3/+3 and this
<b>Spellburst</b> <i>(unless it already
has these effects).</i>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +3/+3 and keywords
    if target:
        
target._attack += 3        target._max_health += 3        target._health += 3