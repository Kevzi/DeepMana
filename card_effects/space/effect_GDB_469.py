"""Effect for Auchenai Death-Speaker (GDB_469).

Card Text: [x]After another friendly
minion is <b>Reborn</b>,
summon a copy of it.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(1):
        game.summon_token(player, "GDB_469t")