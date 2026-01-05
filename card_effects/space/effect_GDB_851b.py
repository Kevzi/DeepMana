"""Effect for Stunning Star (GDB_851b).

Card Text: Choose an enemy minion. It goes <b>Dormant</b> for 2 turns.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Choose an enemy minion. It goes <b>Dormant</b> for 2 turns....
    pass