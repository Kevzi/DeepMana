"""Effect for Expedition Sergeant (GDB_229).

Card Text: [x] <b>Battlecry:</b> The next Draenei 
you play immediately
attacks a random enemy.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x] <b>Battlecry:</b> The next Draenei 
you play immediately
attacks a random enemy....
    pass