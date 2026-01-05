"""Effect for Puzzle Box (VAC_464t12).

Card Text: Transform all minions into random ones that cost (3) more.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Transform all minions into random ones that cost (3) more....
    pass