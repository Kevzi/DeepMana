"""Effect for Flower Power (ETC_373a).

Card Text: Summon five 2/2 Treants.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(2):
        game.summon_token(player, "ETC_373at")