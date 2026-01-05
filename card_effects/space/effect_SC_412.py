"""Effect for Hellion (SC_412).

Card Text: [x]Your other minions
have +1 Attack.
<i>(Transforms if you launched
a <b>Starship</b> this game.)</i>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +1/+0 and keywords
    if target:
        
target._attack += 1