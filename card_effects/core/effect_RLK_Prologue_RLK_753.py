"""Effect for Bonedigger Geist (RLK_Prologue_RLK_753).

Card Text: <b>Battlecry:</b> Spend a <b>Corpse</b> to gain +1/+2.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +1/+2 and keywords
    if target:
        
target._attack += 1        target._max_health += 2        target._health += 2