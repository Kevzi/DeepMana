"""Effect for Amulet of Strides (VAC_959t10).

Card Text: [x]Reduce the Cost of all
cards in your hand by (1).
<i>(Except for spells!)</i>
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]Reduce the Cost of all
cards in your hand by (1).
<i>(Except for spells!)</i>...
    pass