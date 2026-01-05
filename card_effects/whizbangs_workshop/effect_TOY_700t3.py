"""Effect for Deck of Treasures (TOY_700t3).

Card Text: This deck has 5 Treasures in it.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: This deck has 5 Treasures in it....
    pass