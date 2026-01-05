"""Effect for Cup o' Muscle (VAC_338t2).

Card Text: [x]Give a minion in
  your hand +2/+1. 
<i>(Last Drink!)</i>
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +2/+1 and keywords
    if target:
        
target._attack += 2        target._max_health += 1        target._health += 1