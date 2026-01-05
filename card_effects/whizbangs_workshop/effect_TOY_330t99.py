"""Effect for Perfect Module (TOY_330t99).

Card Text: [x]<b>Divine Shield</b>, <b>Taunt</b>,
<b>Lifesteal</b>, <b>Rush</b>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]<b>Divine Shield</b>, <b>Taunt</b>,
<b>Lifesteal</b>, <b>Rush</b>...
    pass