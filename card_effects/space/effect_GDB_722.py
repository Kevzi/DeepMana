"""Effect for Crimson Commander (GDB_722).

Card Text: <b>Battlecry and Deathrattle:</b> Give all Draenei in your
hand +1/+1.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +1/+1 and keywords
    if target:
        
target._attack += 1        target._max_health += 1        target._health += 1


def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent
    # Deathrattle effect
    pass  # TODO: Implement deathrattle portion