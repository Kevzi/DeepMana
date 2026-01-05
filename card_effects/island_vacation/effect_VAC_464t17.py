"""Effect for Staff of Scales (VAC_464t17).

Card Text: Summon three 1/1 Snakes with <b>Rush</b>, <b>Poisonous</b> and <b>Reborn</b>.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(1):
        game.summon_token(player, "VAC_464t17t")