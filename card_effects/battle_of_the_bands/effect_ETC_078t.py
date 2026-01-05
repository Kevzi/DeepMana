"""Effect for Broken Microphone (ETC_078t).

Card Text: Your hero takes 1 additional damage from all sources.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Your hero takes 1 additional damage from all sources....
    pass