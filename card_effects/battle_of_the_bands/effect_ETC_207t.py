"""Effect for Barrel of Monkeys (ETC_207t).

Card Text: Summon a 1/4 Monkey with <b>Taunt</b>.
<i>(2 Monkeys left!)</i>
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(1):
        game.summon_token(player, "ETC_207tt")