"""Effect for Wish (TOY_700t9t2).

Card Text: Wish for the perfect card.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Wish for the perfect card....
    pass