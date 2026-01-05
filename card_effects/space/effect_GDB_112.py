"""Effect for Soulbound Spire (GDB_112).

Card Text: [x]<b>Deathrattle:</b> Summon a
minion with Cost equal to this
minion's Attack <i>(up to 10)</i>.
<b>Starship Piece</b>
"""

from simulator.enums import CardType

def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(1):
        game.summon_token(player, "GDB_112t")