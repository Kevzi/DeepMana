"""Effect for Artanis (SC_754)"""

def battlecry(game, source, target):
    """Battlecry: Discover a Protoss unit. Give it Divine Shield."""
    # Simplified discover
    # Assuming Protoss cards are identified by race or set.
    # Since we don't have a clear "Protoss" race in Enums yet, we'll pick from known SC cards.
    
    protoss_ids = ["SC_753", "SC_754", "SC_762", "SC_755", "SC_756"] # Sample IDs
    
    import random
    chosen_id = random.choice(protoss_ids)
    
    card = game.add_to_hand(source.controller, chosen_id)
    if card:
        card.divine_shield = True
