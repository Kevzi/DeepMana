"""Effect for Saruun (GDB_304).

Card Text: [x]<b>Battlecry:</b> Give all
Elementals in your deck
 <b>Fire Spell Damage +1</b>.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +1/+1 and keywords
    if target:
        
target._attack += 1        target._max_health += 1        target._health += 1