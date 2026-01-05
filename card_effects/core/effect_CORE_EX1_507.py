"""Effect for Murloc Warleader (CORE_EX1_507).

Card Text: Your other Murlocs have +2 Attack.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +2/+0 and keywords
    if target:
        
target._attack += 2