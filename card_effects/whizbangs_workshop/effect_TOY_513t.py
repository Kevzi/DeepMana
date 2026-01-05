"""Effect for Sand Art Elemental (TOY_513t).

Card Text: [x]<b>Mini</b>
<b>Battlecry:</b> Give your hero
+1 Attack and <b>Windfury</b>
this turn.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +1/+0 and keywords
    if target:
        
target._attack += 1
        target._windfury = True