"""Effect for Sandbox Scoundrel (TOY_521t1).

Card Text: [x]<b>Mini</b>
<b>Battlecry:</b> Your next card
this turn costs (2) less.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]<b>Mini</b>
<b>Battlecry:</b> Your next card
this turn costs (2) less....
    pass