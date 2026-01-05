"""Effect for Ship's Chirurgeon (CORE_WON_065).

Card Text: After you summon a minion, give it +1 Health.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(1):
        game.summon_token(player, "CORE_WON_065t")
    # Give +0/+1 and keywords
    if target:
        
target._max_health += 1        target._health += 1
    # Restore 1 Health
    if target:
        game.heal(target, 1, source)