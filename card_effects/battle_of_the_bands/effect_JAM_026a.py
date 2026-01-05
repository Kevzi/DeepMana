"""Effect for Soothing Melody (JAM_026a).

Card Text: [x]Refresh your Hero Power.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]Refresh your Hero Power....
    pass