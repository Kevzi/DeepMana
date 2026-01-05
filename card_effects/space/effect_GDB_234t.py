"""Effect for Replicating Spore (GDB_234t).

Card Text: Summon a random 5-Cost minion. Your future Replicating Spores summon it as well.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon random minion(s)
    import random
    from simulator import CardDatabase
    db = CardDatabase.get_instance()
    minions = [c.card_id for c in db._cards.values() 
               if c.collectible and c.card_type.name == 'MINION']
    for _ in range(5):
        if minions:
            game.summon_token(player, random.choice(minions))