"""Effect for Medivac (SC_403f).

Card Text: [x]<b>Starship Piece</b>
When this is launched,
summon two 2/2 Marines
with <b>Taunt</b>.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(2):
        game.summon_token(player, "SC_403ft")