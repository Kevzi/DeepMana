"""Effect for Siamat (CORE_ULD_178).

Card Text: [x]<b>Battlecry:</b> Gain 2 of <b>Rush</b>,
<b>Taunt</b>, <b>Divine Shield</b>, or
<b>Windfury</b> <i>(your choice).</i>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]<b>Battlecry:</b> Gain 2 of <b>Rush</b>,
<b>Taunt</b>, <b>Divine Shield</b>, or
<b>Windfury</b> <...
    pass