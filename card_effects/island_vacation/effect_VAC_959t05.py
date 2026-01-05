"""Effect for Amulet of Tracking (VAC_959t05).

Card Text: [x]Get 3 random
<b>Legendary</b> cards.
<i>(Then transform them
into <b>Commons</b>!)</i>
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]Get 3 random
<b>Legendary</b> cards.
<i>(Then transform them
into <b>Commons</b>!)</i>...
    pass