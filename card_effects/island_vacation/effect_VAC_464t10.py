"""Effect for Spyglass (VAC_464t10).

Card Text: Put a copy of a random card in your opponent's hand into yours. It costs (3) less.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Put a copy of a random card in your opponent's hand into yours. It costs (3) less....
    pass