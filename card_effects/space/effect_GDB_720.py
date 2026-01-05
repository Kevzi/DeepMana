"""Effect for Starlight Wanderer (GDB_720).

Card Text: <b>Battlecry:</b> The next Draenei you play gains +2/+1.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +2/+1 and keywords
    if target:
        
target._attack += 2        target._max_health += 1        target._health += 1