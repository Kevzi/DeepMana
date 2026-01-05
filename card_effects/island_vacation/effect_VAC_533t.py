"""Effect for Entrée (VAC_533t).

Card Text: <b>Deathrattle:</b> Your opponent summons a minion from their deck.
"""

from simulator.enums import CardType

def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(1):
        game.summon_token(player, "VAC_533tt")