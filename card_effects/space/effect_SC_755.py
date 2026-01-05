"""Effect for Construct Pylons (SC_755).

Card Text: Your next Protoss card this turn costs (2) less.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Your next Protoss card this turn costs (2) less....
    pass