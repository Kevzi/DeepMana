"""Effect for Amulet of Passions (VAC_959t01).

Card Text: Take control of an enemy minion until the end of your turn.
<i>(It has 1 Attack this turn!)</i>
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Take control of an enemy minion until the end of your turn.
<i>(It has 1 Attack this turn!)</i>...
    pass