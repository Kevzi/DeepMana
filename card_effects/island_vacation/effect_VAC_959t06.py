"""Effect for Amulet of Critters (VAC_959t06).

Card Text: Summon a
random 4-Cost minion
and give it <b>Taunt</b>.
<i>(It can't attack!)</i>
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
    for _ in range(4):
        if minions:
            game.summon_token(player, random.choice(minions))
    # Give +4/+0 and keywords
    if target:
        
target._attack += 4
        target._taunt = True