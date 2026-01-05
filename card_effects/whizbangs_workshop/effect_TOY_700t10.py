"""Effect for Deck of Heroes (TOY_700t10).

Card Text: This deck is HEROIC!
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: This deck is HEROIC!...
    pass