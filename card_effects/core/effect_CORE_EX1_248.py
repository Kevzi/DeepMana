"""Effect for Feral Spirit (CORE_EX1_248).

Card Text: Summon two 2/3 Spirit Wolves with <b>Taunt</b>. <b>Overload:</b> (1)
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(2):
        game.summon_token(player, "CORE_EX1_248t")