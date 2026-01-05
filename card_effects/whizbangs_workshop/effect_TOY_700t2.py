"""Effect for Rainbow Deck (TOY_700t2).

Card Text: This deck has cards from all classes and spell schools.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: This deck has cards from all classes and spell schools....
    pass