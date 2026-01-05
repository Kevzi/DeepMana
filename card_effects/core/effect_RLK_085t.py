"""Effect for Risen Golem (RLK_085t).

Card Text: <b>Rush</b>
<i>Doesn't leave a <b>Corpse</b>.</i>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Rush</b>
<i>Doesn't leave a <b>Corpse</b>.</i>...
    pass