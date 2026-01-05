"""Effect for Anachronos (CORE_RLK_919).

Card Text: [x]<b>Battlecry:</b> Send all
other minions 2 turns
into the future.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]<b>Battlecry:</b> Send all
other minions 2 turns
into the future....
    pass