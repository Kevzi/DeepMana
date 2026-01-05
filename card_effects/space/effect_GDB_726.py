"""Effect for Interstellar Starslicer (GDB_726).

Card Text: <b>Battlecry and Deathrattle:</b> Reduce the Cost of your Librams by (1)
this game.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Battlecry and Deathrattle:</b> Reduce the Cost of your Librams by (1)
this game....
    pass


def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent
    # Deathrattle effect
    pass  # TODO: Implement deathrattle portion