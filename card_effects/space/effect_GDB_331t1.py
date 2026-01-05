"""Effect for Splitting Boulder (GDB_331t1).

Card Text: <b>Deathrattle:</b> Summon two 2/2 Splitting Stones.
"""

from simulator.enums import CardType

def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(2):
        game.summon_token(player, "GDB_331t1t")