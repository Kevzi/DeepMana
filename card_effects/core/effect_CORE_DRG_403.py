"""Effect for Blowtorch Saboteur (CORE_DRG_403).

Card Text: <b>Battlecry:</b> Your opponent's next Hero Power costs (2) more.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Battlecry:</b> Your opponent's next Hero Power costs (2) more....
    pass