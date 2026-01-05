"""Effect for Warsong Commander (TOY_409t).

Card Text: Whenever you summon a minion with 3 or less Attack, give it <b>Charge</b>.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(3):
        game.summon_token(player, "TOY_409tt")
    # Give +3/+0 and keywords
    if target:
        
target._attack += 3
        target._charge = True