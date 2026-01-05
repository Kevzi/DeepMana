"""Effect for Space Pirate (GDB_333).

Card Text: <b>Deathrattle:</b> Your next weapon costs (1) less.
"""

from simulator.enums import CardType

def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Deathrattle:</b> Your next weapon costs (1) less....
    pass