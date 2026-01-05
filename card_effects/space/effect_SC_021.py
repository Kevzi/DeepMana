"""Effect for Evolution Chamber (SC_021).

Card Text: Give your minions +1 Attack. Give your Zerg an extra +1/+1.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +1/+1 and keywords
    if target:
        
target._attack += 1        target._max_health += 1        target._health += 1