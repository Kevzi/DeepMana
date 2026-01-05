"""Effect for Dirty Rat (CORE_CFM_790).

Card Text: [x]<b>Taunt</b>
<b>Battlecry:</b> Your opponent
summons a random minion
from their hand.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon random minion(s)
    import random
    from simulator import CardDatabase
    db = CardDatabase.get_instance()
    minions = [c.card_id for c in db._cards.values() 
               if c.collectible and c.card_type.name == 'MINION']
    for _ in range(1):
        if minions:
            game.summon_token(player, random.choice(minions))