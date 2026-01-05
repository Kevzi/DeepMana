"""Effect for Bluesy Totemcarver (JAM_012t2).

Card Text: [x]<b>Battlecry:</b> Summon a
0/3 Mana Tide Totem.
<i>(Changes each turn.)</i>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(0):
        game.summon_token(player, "JAM_012t2t")