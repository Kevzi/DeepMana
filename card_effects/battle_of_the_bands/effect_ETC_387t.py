"""Effect for Rhythm and Roots (ETC_387t).

Card Text: [x]<b>Choose One (Secretly) -</b>
Summon three 5/5
Ancients in 2 turns; or
8/8 Giants in 4 turns.@In 2 turns, summon three 5/5 Ancients <b>(Secretly)</b>.@In 4 turns, summon three 8/8 Giants <b>(Secretly)</b>.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(5):
        game.summon_token(player, "ETC_387tt")