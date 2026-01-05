"""Effect for Bad Omen (GDB_124).

Card Text: In 2 turns, summon two 6/6 Demons with <b>Taunt</b>.
If you're building a <b>Starship</b>, summon them now.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(2):
        game.summon_token(player, "GDB_124t")