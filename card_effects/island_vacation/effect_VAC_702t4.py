"""Effect for Golden Kobold (VAC_702t4).

Card Text: [x]<b>Taunt</b>
<b> Battlecry:</b> Replace your hand
with <b>Legendary</b> minions.
They cost (1) less.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]<b>Taunt</b>
<b> Battlecry:</b> Replace your hand
with <b>Legendary</b> minions.
They cost (1) le...
    pass