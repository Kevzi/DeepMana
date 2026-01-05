"""Effect for The Coin (ETC_COIN1).

Card Text: Gain 1 Mana Crystal this turn only.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Gain 1 Mana Crystal this turn only....
    pass