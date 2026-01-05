"""Effect for Deck of Villains (TOY_700t12).

Card Text: This deck is EVIL!
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: This deck is EVIL!...
    pass