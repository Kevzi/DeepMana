"""Effect for Pylon Module (TOY_330t95).

Card Text: Your other minions
have +1 Attack.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +1/+0 and keywords
    if target:
        
target._attack += 1