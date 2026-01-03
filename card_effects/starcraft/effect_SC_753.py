"""Effect for Photon Cannon (SC_753)"""

def end_turn(game, source):
    """At the end of your turn, deal 2 damage to a random enemy."""
    # Assuming stats are 0/3 Can't Attack ? Usually structures.
    
    enemies = [game.current_player.opponent.hero] + game.current_player.opponent.board
    if enemies:
        import random
        target = random.choice(enemies)
        game.deal_damage(target, 2, source)
