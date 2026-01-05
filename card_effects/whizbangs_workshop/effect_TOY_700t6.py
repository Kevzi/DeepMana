"""Effect for Wonderful Deck (TOY_700t6).

Card Text: Cards in this deck transform into random playable cards each turn while in hand.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Cards in this deck transform into random playable cards each turn while in hand....
    pass