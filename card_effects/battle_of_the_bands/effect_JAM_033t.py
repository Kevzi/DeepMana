"""Effect for Cathedral Musician (JAM_033t).

Card Text: [x]<b>Rush</b>
<b>Divine Shield</b>
<i>(Changes each turn.)</i>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]<b>Rush</b>
<b>Divine Shield</b>
<i>(Changes each turn.)</i>...
    pass