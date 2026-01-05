"""Effect for Slice of Bread (VAC_525t1).

Card Text: <i>Get another Slice of Bread to stuff all minions in between into
a 3-Cost Sandwich!</i>
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <i>Get another Slice of Bread to stuff all minions in between into
a 3-Cost Sandwich!</i>...
    pass