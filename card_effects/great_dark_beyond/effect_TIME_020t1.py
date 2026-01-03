"""Effect for Axe of Cenarius (TIME_020t1)"""

def battlecry(game, source, target):
    """Battlecry: Give your minions +1/+1."""
    for minion in source.controller.board:
        minion.buff(1, 1)
