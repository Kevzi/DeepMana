"""Effect for Ingenious Artificer (GDB_135).

Card Text: [x]  <b>Battlecry:</b> The next Draenei  
you play refreshes Mana
Crystals equal to its Attack.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]  <b>Battlecry:</b> The next Draenei  
you play refreshes Mana
Crystals equal to its Attack....
    pass