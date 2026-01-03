"""Effect for The Ceaseless Expanse (GDB_142)"""

from simulator.enums import Zone

def battlecry(game, source, target):
    """Battlecry: Destroy all minions. Gain a Corpse for each."""
    player = source.controller
    
    # Collect all minions on board (both players)
    minions_to_destroy = []
    
    # Check current player's board
    for minion in game.current_player.board:
        if minion is not source: # Don't destroy self
            minions_to_destroy.append(minion)
            
    # Check opponent's board
    for minion in game.current_player.opponent.board:
        minions_to_destroy.append(minion)
        
    corpses_gained = 0
    
    # Destroy them
    for minion in minions_to_destroy:
        # According to mechanics, killing ANY minion gives a corpse to its owner?
        # But this card says "Gain a Corpse for each". Usually means for the player playing it.
        # Let's assume standard DK mechanic: Friendly death = Corpse.
        # Text "Gain a Corpse for each" implies we gain regardless of whose minion it was.
        
        # Standard destroy
        minion.destroy()
        corpses_gained += 1
        
    # Grant corpses to controller
    if hasattr(player, 'corpses'):
        player.corpses += corpses_gained
    else:
        # Initialize if not present (though Player class usually has it)
        player.corpses = corpses_gained
        
    game.log(f"{source.name} destroyed {len(minions_to_destroy)} minions and gained {corpses_gained} Corpses.")
