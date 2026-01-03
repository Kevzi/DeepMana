"""Effect for Hideous Husk (EDR_810)"""

def battlecry(game, source, target):
    """Battlecry: Gain Reborn."""
    # This might be conditional or native. Assuming unconditional based on text format usually seen.
    # If text is simply "Reborn", it's handled by keywords.
    # If text is "Battlecry: Gain Reborn", it's dynamic.
    source.reborn = True
    
def deathrattle(game, source):
    """Deathrattle: Give a random friendly minion Reborn."""
    friendlies = source.controller.board
    targets = [m for m in friendlies if m is not source and not m.reborn]
    
    if targets:
        import random
        chosen = random.choice(targets)
        chosen.reborn = True
        game.log(f"{source.name} gave Reborn to {chosen.name}")
