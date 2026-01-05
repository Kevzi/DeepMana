"""Effect for Baneling Barrage (SC_001).

Card Text: [x]Get a 1/1 Baneling
that explodes. If you
control a Zerg minion,
get another Baneling.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]Get a 1/1 Baneling
that explodes. If you
control a Zerg minion,
get another Baneling....
    pass