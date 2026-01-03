"""Effect for Infestation (TLC_902)"""

def play(game, source, target):
    """Summon two 1/1 Swarmers with Rush."""
    # Assuming Swarmer ID is TLC_902t
    token_id = "TLC_902t"
    
    for _ in range(2):
        minion = game.summon(source.controller, token_id)
        if minion:
            minion.rush = True
