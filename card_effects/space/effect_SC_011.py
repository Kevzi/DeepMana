"""Effect for Creep Tumor (SC_011).

Card Text: Your Zerg minions have +1 Attack and <b>Rush</b>. Lasts 3 turns.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +1/+3 and keywords
    if target:
        
target._attack += 1        target._max_health += 3        target._health += 3
        target._rush = True