"""Effect for Shrunken Deck (TOY_700t4).

Card Text: This deck only has 20 cards.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: This deck only has 20 cards....
    pass