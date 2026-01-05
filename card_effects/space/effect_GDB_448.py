"""Effect for Murmur (GDB_448).

Card Text: [x]Your first <b>Battlecry</b>
minion each turn costs (1),
but immediately dies
after being played.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]Your first <b>Battlecry</b>
minion each turn costs (1),
but immediately dies
after being played....
    pass