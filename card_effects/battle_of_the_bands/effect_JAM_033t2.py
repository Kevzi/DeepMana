"""Effect for Tropical Musician (JAM_033t2).

Card Text: [x]<b>Rush</b>
<b>Windfury</b>
<i>(Changes each turn.)</i>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]<b>Rush</b>
<b>Windfury</b>
<i>(Changes each turn.)</i>...
    pass