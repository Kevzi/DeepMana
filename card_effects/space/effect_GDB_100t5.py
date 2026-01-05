"""Effect for The Legion's Bane (GDB_100t5).

Card Text: <b>Starship</b>
<i>(Costs (5) Mana to launch.)</i>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Starship</b>
<i>(Costs (5) Mana to launch.)</i>...
    pass