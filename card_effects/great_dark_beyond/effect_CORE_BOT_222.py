"""Effect for Spirit Bomb (CORE_BOT_222)"""

def play(game, source, target):
    """Deal 4 damage to a minion and 4 damage to your hero."""
    if target:
        game.deal_damage(target, 4, source)
        
    game.deal_damage(source.controller.hero, 4, source)
