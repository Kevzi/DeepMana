"""Effect for Rime Sculptor (RLK_Prologue_RLK_752).

Card Text: [x]<b>Battlecry:</b> Summon two
2/1 Rime Elementals with
"<b>Deathrattle:</b> Deal 2 damage
to a random enemy."
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Deal 2 damage to a random enemy
    import random
    targets = list(opponent.board) + ([opponent.hero] if opponent.hero else [])
    if targets:
        game.deal_damage(random.choice(targets), 2, source)
    # Summon random minion(s)
    import random
    from simulator import CardDatabase
    db = CardDatabase.get_instance()
    minions = [c.card_id for c in db._cards.values() 
               if c.collectible and c.card_type.name == 'MINION']
    for _ in range(2):
        if minions:
            game.summon_token(player, random.choice(minions))


def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent
    # Deathrattle effect
    pass  # TODO: Implement deathrattle portion