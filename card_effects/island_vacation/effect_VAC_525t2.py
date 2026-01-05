"""Effect for Minion Sandwich (VAC_525t2).

Card Text: [x]Summon the minions
stuffed in this Sandwich.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(1):
        game.summon_token(player, "VAC_525t2t")