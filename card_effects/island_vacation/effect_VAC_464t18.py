"""Effect for Canopic Jars (VAC_464t18).

Card Text: [x]Give your minions
"<b>Deathrattle:</b> Summon
a random <b>Legendary</b>
minion."
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
    for _ in range(1):
        if minions:
            game.summon_token(player, random.choice(minions))
    # Give +0/+0 and keywords
    if target:
        pass