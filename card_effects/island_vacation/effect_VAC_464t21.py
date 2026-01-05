"""Effect for Dr. Boom's Boombox (VAC_464t21).

Card Text: [x]Summon 7 'Boom Bots'.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(7):
        game.summon_token(player, "VAC_464t21t")