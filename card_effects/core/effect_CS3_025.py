"""Effect for Overlord Runthak (CS3_025).

Card Text: [x]<b>Rush</b>. Whenever this
attacks, give +1/+1 to all
minions in your hand.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +1/+1 and keywords
    if target:
        
target._attack += 1        target._max_health += 1        target._health += 1
        target._rush = True