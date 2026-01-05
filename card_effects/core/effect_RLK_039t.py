"""Effect for Grain Crate (RLK_039t).

Card Text: <b>Casts When Drawn</b>
Summon a 2/2 Undead Peasant.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(2):
        game.summon_token(player, "RLK_039tt")
    # Draw 2 card(s)
    player.draw(2)