"""Effect for Carrier (SC_756).

Card Text: [x]At the end of your turn,
summon four 4/1
Interceptors that attack
random enemies.
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
    for _ in range(4):
        if minions:
            game.summon_token(player, random.choice(minions))