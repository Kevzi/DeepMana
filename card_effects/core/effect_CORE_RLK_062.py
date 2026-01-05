"""Effect for Nerubian Swarmguard (CORE_RLK_062).

Card Text: [x]<b>Taunt</b>
<b>Battlecry:</b> Summon two
copies of this minion.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(1):
        game.summon_token(player, "CORE_RLK_062t")