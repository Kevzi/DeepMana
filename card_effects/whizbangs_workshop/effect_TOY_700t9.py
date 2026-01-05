"""Effect for Deck of Wishes (TOY_700t9).

Card Text: This deck contains 3 Wishes that give you the perfect card.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: This deck contains 3 Wishes that give you the perfect card....
    pass