"""Effect for Resuscitate (TLC_818)"""

def play(game, source, target):
    """Resurrect a friendly minion that died this game."""
    # Simplified: Resurrect random based on graveyard history?
    # Simulator usually tracks graveyard in game.dead_minions
    
    # We need to filter by friendly controller.
    # Assuming game logs or player.graveyard stores dead entities.
    
    # Simple mock if graveyard not fully tracked:
    # (In real engine, we check game.graveyard[player])
    
    # Let's check if player has a graveyard attribute or we use game wide log
    # Assuming valid target is in graveyard.
    
    # Standard Resurrect effect:
    graveyard = getattr(source.controller, 'graveyard', [])
    if graveyard:
        import random
        # Filter for minions
        minions = [c for c in graveyard if c.card_type == 4] # 4 is MINION
        if minions:
            chosen = random.choice(minions)
            game.summon(source.controller, chosen.card_id)
