"""Effect for Copycat Deck (TOY_700t5).

Card Text: This deck is a copy of your opponent's.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: This deck is a copy of your opponent's....
    pass