"""Effect for Viper (SC_018).

Card Text: [x]<b>Battlecry:</b> Summon a minion
from your opponent's hand.
Your other Zerg minions gain
<b>Reborn</b> and attack it.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(1):
        game.summon_token(player, "SC_018t")