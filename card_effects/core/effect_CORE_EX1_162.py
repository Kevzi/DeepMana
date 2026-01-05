"""Effect for Dire Wolf Alpha (CORE_EX1_162).

Card Text: Adjacent minions have +1 Attack.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +1/+0 and keywords
    if target:
        
target._attack += 1