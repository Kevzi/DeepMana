"""Effect for Escape Pod (GDB_877).

Card Text: [x]<b>Rush</b>
 <b>Deathrattle:</b> Give adjacent 
minions +1/+1 and <b>Rush</b>.
"""

from simulator.enums import CardType

def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent

    # Give +1/+1 and keywords
    if target:
        
target._attack += 1        target._max_health += 1        target._health += 1
        target._rush = True