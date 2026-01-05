"""Effect for Wax Rager (VAC_464t22).

Card Text: <b>Deathrattle:</b> Resummon this minion.
"""

from simulator.enums import CardType

def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(1):
        game.summon_token(player, "VAC_464t22t")