"""Effect for Crystalline Greatmace (GDB_231).

Card Text: After your hero attacks, give all Draenei in your hand +2 Attack.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +2/+0 and keywords
    if target:
        
target._attack += 2