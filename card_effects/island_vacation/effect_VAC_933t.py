"""Effect for Parachute (VAC_933t).

Card Text: <b>Casts When Drawn</b>
Summon a 1/1 Pirate with <b>Charge</b>.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(1):
        game.summon_token(player, "VAC_933tt")
    # Draw 1 card(s)
    player.draw(1)