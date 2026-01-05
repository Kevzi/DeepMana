"""Effect for Lift Off (SC_410).

Card Text: Draw 2 Terran cards. Summon a 2/1 <b>Starship Piece</b> with an effect when launched.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(2):
        game.summon_token(player, "SC_410t")
    # Draw 2 card(s)
    player.draw(2)