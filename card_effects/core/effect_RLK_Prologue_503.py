"""Effect for Body Bagger (RLK_Prologue_503).

Card Text: <b>Battlecry</b>: Gain a <b>Corpse</b>.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Battlecry</b>: Gain a <b>Corpse</b>....
    pass