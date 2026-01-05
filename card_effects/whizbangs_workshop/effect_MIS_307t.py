"""Effect for Molded Tinyfin (MIS_307t).

Card Text: <b>Rush</b>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Rush</b>...
    pass