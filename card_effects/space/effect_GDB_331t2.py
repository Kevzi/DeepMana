"""Effect for Splitting Stone (GDB_331t2).

Card Text: <b>Deathrattle:</b> Summon two 1/1 Pebbles.
"""

from simulator.enums import CardType

def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(1):
        game.summon_token(player, "GDB_331t2t")