"""Effect for Shaladrassil (EDR_846)"""

def battlecry(game, source, target):
    """Battlecry: Restore full Health to your hero."""
    player = source.controller
    if player.hero:
        missing_health = player.hero.max_health - player.hero.health
        if missing_health > 0:
            game.heal(player.hero, missing_health, source)
