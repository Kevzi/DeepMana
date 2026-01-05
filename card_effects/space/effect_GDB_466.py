"""Effect for The Gravitational Displacer (GDB_466).

Card Text: [x]<b>Starship Piece</b>
When this is launched,
summon a copy of
the <b>Starship</b>.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon a copy of this minion
    if source.card_id:
        game.summon_token(player, source.card_id)