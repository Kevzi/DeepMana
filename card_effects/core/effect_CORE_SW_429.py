"""Effect for Best in Shell (CORE_SW_429).

Card Text: [x]<b>Tradeable</b>
Summon two 2/7
 Turtles with <b>Taunt</b>.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(2):
        game.summon_token(player, "CORE_SW_429t")