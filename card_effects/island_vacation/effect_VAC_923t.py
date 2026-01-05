"""Effect for Sanc'Azel (VAC_923t).

Card Text: [x]Give a friendly minion
+3 Attack and <b>Rush</b>.
Turn back into a minion.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +3/+0 and keywords
    if target:
        
target._attack += 3
        target._rush = True