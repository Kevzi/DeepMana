"""Effect for Finja, the Flying Star (CORE_CFM_344).

Card Text: [x]<b>Stealth</b>
   Whenever this attacks and   
kills a minion, summon 2
 Murlocs from your deck.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(2):
        game.summon_token(player, "CORE_CFM_344t")