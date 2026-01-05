"""Effect for Nostalgic Initiate (TOY_340t1).

Card Text: <b>Mini</b>
The first time you cast a spell, gain +2/+2.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +2/+2 and keywords
    if target:
        
target._attack += 2        target._max_health += 2        target._health += 2