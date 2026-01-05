"""Effect for Dread Corsair (CORE_NEW1_022).

Card Text: <b>Taunt</b>
Costs (1) less per Attack of your weapon.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Taunt</b>
Costs (1) less per Attack of your weapon....
    pass