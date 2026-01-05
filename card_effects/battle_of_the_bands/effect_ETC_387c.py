"""Effect for Giant's Dance (ETC_387c).

Card Text: In 4 turns, summon three 8/8 Giants <b>(Secretly)</b>.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(4):
        game.summon_token(player, "ETC_387ct")