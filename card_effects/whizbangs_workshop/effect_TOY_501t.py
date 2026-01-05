"""Effect for Shudderblock (TOY_501t).

Card Text: [x]<b>Mini</b>
<b>Battlecry:</b> Your next <b>Battlecry</b>
triggers 3 times, but can't
 damage the enemy hero.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]<b>Mini</b>
<b>Battlecry:</b> Your next <b>Battlecry</b>
triggers 3 times, but can't
 damage the ...
    pass