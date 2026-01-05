"""Effect for Mountain Bear (CORE_AV_337).

Card Text: [x]<b>Taunt</b>
<b>Deathrattle:</b> Summon two
2/4 Cubs with <b>Taunt</b>.
"""

from simulator.enums import CardType

def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(2):
        game.summon_token(player, "CORE_AV_337t")