"""Effect for Infernal Stratagem (GDB_122).

Card Text: [x]Give a minion +3/+3.
If it's a Demon, your
next one costs (2) less.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +3/+3 and keywords
    if target:
        
target._attack += 3        target._max_health += 3        target._health += 3