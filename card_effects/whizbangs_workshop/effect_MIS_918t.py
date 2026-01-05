"""Effect for Flickering Lightbot (MIS_918t).

Card Text: [x]<b>Gigantic</b>
Costs (1) less for each
Holy spell you've cast
this game.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]<b>Gigantic</b>
Costs (1) less for each
Holy spell you've cast
this game....
    pass