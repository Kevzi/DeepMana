"""Effect for Ancient's Melody (ETC_387b).

Card Text: In 2 turns, summon three 5/5 Ancients <b>(Secretly)</b>.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(2):
        game.summon_token(player, "ETC_387bt")