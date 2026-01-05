"""Effect for Amulet of Passions (VAC_959t01t).

Card Text: Take control of an enemy minion until the end of your turn.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Take control of an enemy minion until the end of your turn....
    pass