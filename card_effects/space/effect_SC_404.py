"""Effect for Salvage the Bunker (SC_404).

Card Text: Summon two 2/2 Marines with <b>Taunt</b>.
Your next <b>Starship</b>
launch costs (2) less.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(2):
        game.summon_token(player, "SC_404t")