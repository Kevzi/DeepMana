"""Effect for Murloc Growfin (MIS_307t1).

Card Text: [x]<b>Gigantic</b>
<b>Battlecry:</b> Summon a
Tinyfin with <b>Rush</b> and stats
equal to this minion's.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(1):
        game.summon_token(player, "MIS_307t1t")