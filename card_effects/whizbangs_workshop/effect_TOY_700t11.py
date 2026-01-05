"""Effect for Deck of Legends (TOY_700t11).

Card Text: This deck is full of two copies of <b>Legendary</b> cards.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: This deck is full of two copies of <b>Legendary</b> cards....
    pass