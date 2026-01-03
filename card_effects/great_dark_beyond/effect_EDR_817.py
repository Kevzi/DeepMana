"""Effect for Sanguine Infestation (EDR_817)"""

def play(game, source, target):
    """Lifesteal. Deal 2 damage to all minions."""
    # Source (Spell) has Lifesteal.
    damage = 2
    
    # Collect targets first (snapshot)
    targets = []
    for player in game.players:
        targets.extend(player.board)
        
    for minion in targets:
        game.deal_damage(minion, damage, source)
