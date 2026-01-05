"""Effect for Hilt of Quel'Delar (VAC_464t30).

Card Text: Give a minion +3/+3.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +3/+3 and keywords
    if target:
        
target._attack += 3        target._max_health += 3        target._health += 3