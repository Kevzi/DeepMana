"""Effect for Conflagrate (FIR_954)"""

def play(game, source, target):
    """Deal 3 damage to a minion and its neighbors."""
    if target:
        # Main target
        game.deal_damage(target, 3, source)
        
        # Neighbors
        neighbors = source.controller.opponent.get_neighbors(target) # Assuming target is enemy
        # Actually logic ensures we get neighbors regardless of controller
        # Need board index logic.
        
        # If simulation exposes get_neighbors on board state:
        board = target.controller.board
        if target in board:
            idx = board.index(target)
            if idx > 0:
                game.deal_damage(board[idx-1], 3, source)
            if idx < len(board) - 1:
                game.deal_damage(board[idx+1], 3, source)
