"""Effect for Grave Strength (RLK_Prologue_RLK_707).

Card Text: [x]Give your minions +1
Attack. Spend 5 <b>Corpses</b>
to give them +3 instead.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +1/+5 and keywords
    if target:
        
target._attack += 1        target._max_health += 5        target._health += 5