"""Effect for Bad Omen (GDB_124t).

Card Text: [x]In 2 turns, summon two
6/6 Demons with <b>Taunt</b>.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(2):
        game.summon_token(player, "GDB_124tt")