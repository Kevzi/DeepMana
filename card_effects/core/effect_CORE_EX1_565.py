"""Effect for Flametongue Totem (CORE_EX1_565).

Card Text: Adjacent minions have +2 Attack.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +2/+0 and keywords
    if target:
        
target._attack += 2