"""Effect for The Astral Compass (GDB_100t7).

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