"""Effect for Risen Footman (RLK_061t).

Card Text: <b>Taunt</b>
<i>Doesn't leave a <b>Corpse</b>.</i>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Taunt</b>
<i>Doesn't leave a <b>Corpse</b>.</i>...
    pass