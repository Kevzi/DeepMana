"""Effect for Movement of Sloth (ETC_085t8).

Card Text: Summon a 6/6 Demon with <b>Taunt</b> and <b>Reborn</b>.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(6):
        game.summon_token(player, "ETC_085t8t")