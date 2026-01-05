"""Effect for Red Giant (GDB_341).

Card Text: Costs (1) less for each adjacent card played while in hand.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Costs (1) less for each adjacent card played while in hand....
    pass