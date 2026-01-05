"""Effect for Novice Zapper (CS3_007).

Card Text: <b>Spell Damage +1</b> <b>Overload:</b> (1)
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +1/+1 and keywords
    if target:
        
target._attack += 1        target._max_health += 1        target._health += 1