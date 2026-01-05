"""Effect for Tigress Plushy (TOY_811t).

Card Text: <b>Mini</b>
<b>Rush</b>, <b>Lifesteal</b>,
<b>Divine Shield</b>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Mini</b>
<b>Rush</b>, <b>Lifesteal</b>,
<b>Divine Shield</b>...
    pass