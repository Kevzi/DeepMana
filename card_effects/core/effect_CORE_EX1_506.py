"""Effect for Murloc Tidehunter (CORE_EX1_506).

Card Text: <b>Battlecry:</b> Summon a 1/1 Murloc Scout.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(1):
        game.summon_token(player, "CORE_EX1_506t")