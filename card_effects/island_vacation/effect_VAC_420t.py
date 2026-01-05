"""Effect for Fortune (VAC_420t).

Card Text: This is a copy of the top card of your deck.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: This is a copy of the top card of your deck....
    pass