"""Effect for Starport (SC_403).

Card Text: [x]Summon a 2/1
<b>Starship Piece</b> with an
effect when launched.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(2):
        game.summon_token(player, "SC_403t")