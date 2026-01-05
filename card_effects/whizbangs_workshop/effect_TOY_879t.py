"""Effect for Repackaged Box (TOY_879t).

Card Text: [x]Add the resealed
minions to your hand.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]Add the resealed
minions to your hand....
    pass