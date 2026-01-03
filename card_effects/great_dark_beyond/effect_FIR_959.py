"""Effect for Fyrakk the Blazing (FIR_959)"""

def battlecry(game, source, target):
    """Battlecry: Deal 4 damage to all minions. Usually adds a weapon too."""
    # Assuming simple version: damage all
    for minion in game.board:
        game.deal_damage(minion, 4, source)
