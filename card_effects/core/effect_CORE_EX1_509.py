"""Effect for Murloc Tidecaller (CORE_EX1_509).

Card Text: Whenever you summon a Murloc, gain +1 Attack.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(1):
        game.summon_token(player, "CORE_EX1_509t")
    # Give +1/+0 and keywords
    if target:
        
target._attack += 1