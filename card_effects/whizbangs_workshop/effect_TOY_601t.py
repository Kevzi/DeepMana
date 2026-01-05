"""Effect for Factory Assemblybot (TOY_601t).

Card Text: <b>Mini</b>
At the end of your turn, summon a 6/7 Bot that attacks a random enemy.
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
    for _ in range(6):
        if minions:
            game.summon_token(player, random.choice(minions))