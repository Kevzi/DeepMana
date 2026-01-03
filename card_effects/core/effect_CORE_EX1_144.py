
from simulator.entities import Card
from simulator.player import Player
from simulator.game import Game

def on_play(game: Game, player: Player, card: Card, target=None):
    if target and target.owner == player:
        # Remove from board
        player.board.remove(target)
        # Reset stats but keep card ID
        target.reset() # This normally resets temp stats/enchantments
        # Set reduction
        target.mod_cost -= 2
        # Add back to hand
        player.add_to_hand(target)
