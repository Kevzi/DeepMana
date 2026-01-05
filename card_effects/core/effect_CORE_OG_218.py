"""Effect for Bloodhoof Brave (CORE_OG_218).

Card Text: <b>Taunt</b>
Has +3 Attack while damaged.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +3/+0 and keywords
    if target:
        
target._attack += 3
        target._taunt = True