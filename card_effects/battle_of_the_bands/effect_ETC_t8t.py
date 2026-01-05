"""Effect for Bored Doomlord (ETC_t8t).

Card Text: [x]<b>Taunt</b>
<b>Reborn</b>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]<b>Taunt</b>
<b>Reborn</b>...
    pass