"""Effect for Hellbat (SC_412t).

Card Text: Your other minions have +2 Attack and <b>Rush</b>.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +2/+0 and keywords
    if target:
        
target._attack += 2
        target._rush = True