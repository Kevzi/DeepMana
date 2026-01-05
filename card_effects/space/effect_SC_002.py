"""Effect for Infestor (SC_002).

Card Text: [x]<b>Deathrattle:</b> Your Zerg
minions have +1 Attack for
the rest of the game.
"""

from simulator.enums import CardType

def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent

    # Give +1/+0 and keywords
    if target:
        
target._attack += 1