"""Effect for Shadow Ascendant (CORE_ICC_210).

Card Text: [x]At the end of your turn,
give another random
friendly minion +1/+1.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +1/+1 and keywords
    if target:
        
target._attack += 1        target._max_health += 1        target._health += 1