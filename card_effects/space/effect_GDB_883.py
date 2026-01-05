"""Effect for Distress Signal (GDB_883).

Card Text: [x]Summon two random
2-Cost minions.
Refresh 2 Mana Crystals.
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
    for _ in range(2):
        if minions:
            game.summon_token(player, random.choice(minions))