"""Effect for Inspirational Lyrics (JAM_026b).

Card Text: Your next Hero Power costs (0).
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Your next Hero Power costs (0)....
    pass