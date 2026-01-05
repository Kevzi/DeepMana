"""Effect for Bubba (VAC_464t6).

Card Text: [x]<b>Battlecry</b>: Summon six
1/1 Bloodhounds with
<b>Rush</b> to attack an
enemy minion.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(1):
        game.summon_token(player, "VAC_464t6t")