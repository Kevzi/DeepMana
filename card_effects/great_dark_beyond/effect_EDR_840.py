"""Effect for Grim Harvest (EDR_840)"""

def play(game, source, target):
    """Destroy a friendly minion. Deal 4 damage to a random enemy minion."""
    if target and target.controller == source.controller:
        target.destroy()
        
        enemies = source.controller.opponent.board
        if enemies:
            import random
            victim = random.choice(enemies)
            game.deal_damage(victim, 4, source)
