"""Effect for Menagerie Jug (CORE_WON_142).

Card Text: [x]<b>Battlecry:</b> Give 3 random
friendly minions of different
minion types +2/+2.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +3/+2 and keywords
    if target:
        
target._attack += 3        target._max_health += 2        target._health += 2