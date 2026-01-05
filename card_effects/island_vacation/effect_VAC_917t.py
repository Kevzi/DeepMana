"""Effect for Sunscreen (VAC_917t).

Card Text: Give a minion +1/+2.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +1/+2 and keywords
    if target:
        
target._attack += 1        target._max_health += 2        target._health += 2