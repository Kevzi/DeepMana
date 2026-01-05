"""Effect for Careful Bear (WORK_024t).

Card Text: <b>Taunt</b>
At the start of your turn,
if this is in your hand, gain +1/+1.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +1/+1 and keywords
    if target:
        
target._attack += 1        target._max_health += 1        target._health += 1
        target._taunt = True