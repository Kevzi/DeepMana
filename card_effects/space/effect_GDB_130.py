"""Effect for Crystal Welder (GDB_130).

Card Text: [x]<b>Taunt</b>
<b>Battlecry:</b> If you're building
a <b>Starship</b>, gain +2/+2.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +2/+2 and keywords
    if target:
        
target._attack += 2        target._max_health += 2        target._health += 2
        target._taunt = True