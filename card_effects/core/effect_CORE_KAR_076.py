"""Effect for Firelands Portal (CORE_KAR_076).

Card Text: Deal $6 damage. Summon a random
6-Cost minion.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Deal 6 damage to a random character
    import random
    targets = list(player.board) + list(opponent.board)
    if player.hero: targets.append(player.hero)
    if opponent.hero: targets.append(opponent.hero)
    if targets:
        game.deal_damage(random.choice(targets), 6, source)
    # Summon random minion(s)
    import random
    from simulator import CardDatabase
    db = CardDatabase.get_instance()
    minions = [c.card_id for c in db._cards.values() 
               if c.collectible and c.card_type.name == 'MINION']
    for _ in range(6):
        if minions:
            game.summon_token(player, random.choice(minions))