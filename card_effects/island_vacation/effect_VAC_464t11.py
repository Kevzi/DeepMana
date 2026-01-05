"""Effect for Clockwork Assistant (VAC_464t11).

Card Text: Has +1/+1 for each spell you've cast this game.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +1/+1 and keywords
    if target:
        
target._attack += 1        target._max_health += 1        target._health += 1