"""Effect for Stitched Giant (RLK_Prologue_RLK_744).

Card Text: [x]Costs (1) less for each
<b>Corpse</b> you've spent
this game.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]Costs (1) less for each
<b>Corpse</b> you've spent
this game....
    pass