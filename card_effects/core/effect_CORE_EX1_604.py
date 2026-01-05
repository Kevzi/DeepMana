"""Effect for Frothing Berserker (CORE_EX1_604).

Card Text: Whenever a minion takes damage, gain +1 Attack.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +1/+0 and keywords
    if target:
        
target._attack += 1