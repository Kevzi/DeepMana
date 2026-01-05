"""Effect for Frostmourne (CORE_RLK_086).

Card Text: <b>Deathrattle:</b> Summon every minion killed by this weapon.
"""

from simulator.enums import CardType

def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(1):
        game.summon_token(player, "CORE_RLK_086t")