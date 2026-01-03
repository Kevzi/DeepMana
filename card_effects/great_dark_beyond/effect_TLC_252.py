"""Effect for Dissolving Ooze (TLC_252)"""

def battlecry(game, source, target):
    """Battlecry: Destroy your opponent's weapon."""
    # Ooze effect
    opponent = source.controller.opponent
    if opponent.weapon:
        opponent.weapon.destroy()
