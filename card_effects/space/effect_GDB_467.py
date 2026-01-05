"""Effect for Quasar (GDB_467).

Card Text: Shuffle your hand into your deck.
Reduce the Cost of cards in your deck by (3).
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Shuffle your hand into your deck.
Reduce the Cost of cards in your deck by (3)....
    pass