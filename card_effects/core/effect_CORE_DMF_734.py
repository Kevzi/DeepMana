"""Effect for Greybough (CORE_DMF_734).

Card Text: [x]<b>Taunt</b>
<b>Deathrattle:</b> Give a random
friendly minion "<b>Deathrattle:</b>
Summon Greybough."
"""

from simulator.enums import CardType

def deathrattle(game, source):
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
    # Give +0/+0 and keywords
    if target:
        pass
        target._taunt = True